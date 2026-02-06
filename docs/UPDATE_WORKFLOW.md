# Update Workflow (LAN MVP + Safe)

Target Environment: LAN (Local Area Network)
Shared Path: `\\10.1.3.2\KEIToolsData\SpreadSheetCompare`

Mục tiêu: triển khai cập nhật nội bộ đơn giản nhưng **an toàn tối thiểu** (không bị "bán cập nhật" và có kiểm tra integrity), phù hợp cho giai đoạn nhỏ trong LAN.

## 1. Kiến trúc tổng quan (Pull-based)
Client tự kiểm tra update từ share LAN. Mỗi bản phát hành nằm trong **folder version riêng** để update atomic và dễ rollback.

### Repository Layout (khuyến nghị)
```
\\10.1.3.2\KEIToolsData\SpreadSheetCompare\
  LATEST.txt
  releases\
    1.0.1\
      version.json
      package.zip                # Khuyến nghị (1-file) hoặc dùng folder app/
      app\                        # Tuỳ chọn nếu không dùng zip
        DocCompareAI.exe
        _internal\
        assets\
      updater\
        Updater.exe
    1.0.2\
      ...
  changelog\
    1.0.1.txt
    1.0.2.txt
```

**Lý do dùng `LATEST.txt`:** update an toàn bằng cách upload release mới xong rồi **chỉ đổi LATEST.txt** ở cuối.

## 2. Manifest phiên bản (`version.json`)
Dùng **một nguồn version duy nhất**. Ví dụ:
```json
{
  "version": "1.0.1",
  "release_date": "2026-02-10",
  "notes": "Fixed font size crash; Improved Ribbon UI.",
  "package": {
    "path": "package.zip",
    "sha256": "<sha256-hex>",
    "size": 12345678
  },
  "app_exe": "DocCompareAI.exe"
}
```
Nếu không dùng `package.zip`, thay bằng:
```json
"package": { "path": "app/", "sha256": "<sha256-of-folder-or-omit>" }
```

## 3. Quy trình phát hành (Server Side)
1. Build app (one-folder) → đóng gói thành `package.zip` (khuyến nghị).
2. Tạo `version.json` và tính `sha256` cho `package.zip`.
3. Upload vào `releases/<version>/`.
4. **Cập nhật `LATEST.txt` cuối cùng** (ghi version mới).

## 3A. Kế hoạch triển khai từng phần (từ code → build → release)
Mục tiêu: có checklist rõ ràng cho từng bước để tránh thiếu file hoặc cập nhật lỗi.

### Giai đoạn 1: Chuẩn bị code
1. Hoàn thiện tính năng và fix bug cần phát hành.
2. Cập nhật `VERSION.txt` (source of truth) nếu cần đổi version (major/minor).
3. `core/version.py` sẽ đọc từ `VERSION.txt` tự động.
3. Cập nhật `docs/UPDATE_WORKFLOW.md` nếu thay đổi luồng.
4. Cập nhật changelog tương ứng (ví dụ: `changelog/1.0.1.txt`).

### Giai đoạn 2: Build nội bộ (local)
1. Build app theo quy trình hiện tại (`build_app.bat`).
   - Script sẽ sync version từ `VERSION.txt` → `core/version.py`.
   - Build xong sẽ copy `VERSION.txt` vào `dist/DocCompareAI/` để publish kiểm tra version.
2. Kiểm tra output: `DocCompareAI.exe`, `_internal/`, `assets/` (nếu dùng one-folder).
3. Chạy thử app ở máy build để đảm bảo launch và chức năng chính ổn.

### Giai đoạn 3: Đóng gói + tạo manifest
1. Nén toàn bộ output thành `package.zip`.
2. Tạo `version.json` và điền đúng:
   - `version`, `release_date`, `notes`
   - `package.path = "package.zip"`
   - `package.sha256` + `package.size`
   - `app_exe` = `DocCompareAI.exe`

### Giai đoạn 4: Upload lên remote_root (share LAN)
1. Tạo thư mục `releases/<version>/` trên `remote_root`.
2. Upload `package.zip`, `version.json`, `Updater.exe` (nếu thay đổi) vào đúng folder.
3. Upload changelog vào `changelog/<version>.txt`.
4. Upload file cài đặt vào `installers/` theo đúng tên phiên bản.
5. **Chưa cập nhật `LATEST.txt` ở bước này.**

### Giai đoạn 5: Kiểm tra phát hành
1. Trên 1 máy test, đổi `LATEST.txt` tạm thời (hoặc trỏ thủ công) để thử update.
2. Kiểm tra: tải package, verify hash, update thành công, app chạy bình thường.
3. Nếu lỗi: giữ nguyên `LATEST.txt`, sửa lại release và re-upload.

### Giai đoạn 6: Publish chính thức
1. Cập nhật `LATEST.txt` = phiên bản mới.
2. Theo dõi log/feedback trong ngày đầu để phát hiện lỗi sớm.

### Giai đoạn 7: Rollback (khi cần)
1. Đổi `LATEST.txt` về version cũ.
2. Nếu cần, xoá release lỗi hoặc giữ lại để điều tra.

## 4. Logic phía Client (Python)
- Chạy **async** khi startup hoặc theo nút “Update”.
- Đọc `LATEST.txt` để biết version mới nhất.
- Đọc `releases/<version>/version.json` để lấy metadata.
- So sánh semver.

Pseudo-code:
```python
remote_root = r"\\10.1.3.2\KEIToolsData\SpreadSheetCompare"
LATEST_FILE = os.path.join(remote_root, "LATEST.txt")

CURRENT_VERSION = "1.0.0"

def check_update():
    try:
        latest = open(LATEST_FILE, "r", encoding="utf-8").read().strip()
        if not latest:
            return None
        manifest_path = os.path.join(remote_root, "releases", latest, "version.json")
        data = json.load(open(manifest_path, "r", encoding="utf-8"))
        if parse_version(data["version"]) > parse_version(CURRENT_VERSION):
            return data, latest
    except Exception:
        return None
```

## 5. Updater.exe (Separate Process)
Updater cần **đợi app đóng thật sự**, copy vào staging, verify hash, rồi swap.

### Quy trình đề xuất
1. Wait process exit (poll `DocCompareAI.exe`).
2. Copy `package.zip` về `LOCAL_TEMP`.
3. Verify `sha256`.
4. Extract vào `install_dir\.update_staging`.
5. Rename folder cũ → `app.bak` (hoặc `version_old`).
6. Move staging → `app`.
7. Launch exe mới.
8. Nếu lỗi, rollback từ `app.bak`.

Pseudo-code (rút gọn):
```python
# Args: release_dir, install_dir
wait_for_process_exit(app_exe)
copy(package.zip -> temp)
verify_sha256(temp, expected)
extract(temp -> staging)
rename(app -> app.bak)
move(staging -> app)
launch(app_exe)
```

## 6. Tối thiểu hóa rủi ro (LAN MVP)
- **Hash check bắt buộc** để tránh file hỏng/ghi dang dở.
- `LATEST.txt` chỉ đổi sau khi upload xong.
- Updater chạy ngoài app chính.
- Rollback khi update fail.

## 7. Permissions
- User chỉ cần **Read** trên share.
- Admin/publisher cần **Write** vào share.
- App nên cài trong thư mục user-writable (ví dụ `AppData\Local\Programs\...`).

## 8. Gợi ý mở rộng sau này (không bắt buộc)
- Ký số `Updater.exe` / `DocCompareAI.exe`.
- Gửi `package.sig` và verify signature.
- Thêm API web update hoặc CDN (nếu triển khai rộng).

## 9. Workflow thực tế bằng script
### Build
- Chạy: `build_app.bat`

### Publish
- Chuẩn bị file cài đặt đúng tên:
  - `installer/DocCompareAI_Setup_v<version>.exe`
- Chạy: `publish_release.bat`
  - Script sẽ tự zip, hash, tạo `version.json`, copy lên `remote_root`
  - Nếu installer không đúng version → **dừng và nhắc build Inno**
  - Sau khi publish thành công → **tự tăng patch version** (vd `1.0.1 → 1.0.2`)

---

## 10. Luồng tiếp nhận feedback (giai đoạn đầu)
Mục tiêu: thu thập phản hồi của user để cải tiến UX, tính năng và update flow.

### MVP (hiện tại)
- Trong app có nút `Feedback`.
- Feedback được lưu dạng JSONL tại:
  - `C:\Users\<user>\.spreadsheet_compare\feedback\feedback.jsonl`
- App sẽ **thử sync** feedback lên share LAN nếu có quyền:
  - `\\10.1.3.2\KEIToolsData\SpreadSheetCompare\feedback\feedback_<machine>_<user>.jsonl`

### Kế hoạch cải tiến (sắp tới)
1. Chuẩn hóa định dạng log (JSON line), ví dụ:
   ```json
   {"time":"2026-02-06 14:45:10","user":"<optional>","type":"bug|idea|ui","message":"..."}
   ```
2. Sync feedback lên share LAN:
   - Thêm folder `\\10.1.3.2\\KEIToolsData\\SpreadSheetCompare\\feedback\\`
   - App ghi log local → định kỳ copy lên share (hoặc gửi trực tiếp nếu có quyền).
3. Có màn hình tổng hợp feedback:
   - Lọc theo loại (bug/idea/ui)
   - Ưu tiên theo số lượt trùng.
4. Tạo checklist cải tiến dựa trên feedback định kỳ (weekly).

---

### Tóm tắt nhanh
- **Dùng `LATEST.txt` + `releases/<version>/` để update an toàn.**
- **Bắt buộc hash check** và **rollback**.
- **1 nguồn version duy nhất (`version.json`).**

Đây là phiên bản tối ưu cho LAN nhỏ nhưng vẫn an toàn. Khi bạn muốn mở rộng ra Internet, phần `package.sig`/signature là bước cần thêm đầu tiên.
