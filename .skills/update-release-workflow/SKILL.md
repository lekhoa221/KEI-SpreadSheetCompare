---
name: update-release-workflow
description: Chuẩn hóa, triển khai, và review luồng update release an toàn cho ứng dụng desktop Python trong LAN (build, package.zip, version.json, publish, LATEST.txt, updater). Dùng khi người dùng yêu cầu tạo mới/sửa/refactor/review quy trình cập nhật, xử lý mismatch version/hash, hoặc thiết lập checklist phát hành. Không dùng cho cloud deployment, CI/CD internet-first, hoặc yêu cầu không liên quan đến update lifecycle.
---

# Update Release Workflow

### Muc dich cua skill

* **Mục tiêu chính** của skill này là biến yêu cầu "cập nhật phiên bản" thành quy trình release có kiểm soát và có thể lặp lại.
* Skill giúp **giảm lỗi publish**, đồng bộ version nhất quán, và rút ngắn thời gian release thông qua checklist + script preflight.

### Khi nao dung skill nay?

* **Điều kiện 1:** Khi người dùng yêu cầu tạo mới/sửa/review luồng update, phát hành version, rollback, hoặc kiểm tra lỗi cập nhật.
* **Điều kiện 2:** Khi project là ứng dụng desktop Python (PyInstaller) phát hành qua share LAN với `LATEST.txt` + `releases/<version>/`.
* **Không dùng:** Khi bài toán thuộc cloud deployment, container orchestration, mobile OTA, hoặc yêu cầu mơ hồ không liên quan release/update.

### Quy trinh hoat dong (step-by-step)

1.  **Phân tích yêu cầu**
    * Xác định yêu cầu là:
        * [ ] Tạo mới
        * [ ] Sửa / refactor
        * [ ] Review / kiểm tra
        * [ ] Khác
    * Xác định phạm vi tác động: script build/publish, updater, tài liệu release, hay chỉ checklist.
    * Đọc nhanh các file context chính: `VERSION.txt`, `publish_release.bat`, `build_app.bat`, `core/update_manager.py`, `docs/UPDATE_WORKFLOW.md`.

2.  **Chuẩn bị / điều kiện**
    * Xác định stack và môi trường:
        * Python + PyInstaller
        * Batch/PowerShell trên Windows
        * LAN share root (`REMOTE_ROOT`) và local release root (`releases/`)
    * Chạy preflight trước khi publish:
        * `powershell -ExecutionPolicy Bypass -File .skills/update-release-workflow/scripts/preflight_update.ps1 -ProjectRoot .`
    * Nếu release chính thức cần installer:
        * `powershell -ExecutionPolicy Bypass -File .skills/update-release-workflow/scripts/preflight_update.ps1 -ProjectRoot . -RequireInstaller`

3.  **Thực hiện tác vụ chính**
    * Tuân thủ release protocol trong `references/guideline.md`.
    * **Full release:**
        * Chạy `build_app.bat`
        * Chạy `build_installer.bat` (nếu cần installer)
        * Chạy `publish_release.bat`
    * **Quick local update test:** Làm theo `docs/quick_update_test.md` để test nhanh không bị build loop.
    * Nếu cần tạo file mới: Dùng template `assets/version.json.template` cho manifest.
    * Nếu cần review: Dùng checklist trong `references/checklist.md` và đánh dấu từng mục pass/fail.

4.  **Kiểm tra / tối ưu**
    * Kiểm tra tính nhất quán version (`VERSION.txt`, `dist/DocCompareAI/VERSION.txt`, `version.json`).
    * Kiểm tra hash và package metadata trong `version.json`.
    * Kiểm tra sequencing publish để tránh "bản cập nhật lỗi": **Upload `package.zip` + `version.json` + updater xong mới đổi `LATEST.txt`**.
    * Đề xuất cải tiến nếu thấy anti-pattern, không sửa bừa các file nhạy cảm.

### Cac quy tac bat buoc (hard rules)

* [ ] Frontmatter chỉ gồm `name` và `description`; không thêm metadata khác trong `SKILL.md`.
* [ ] Sử dụng một nguồn version chính là `VERSION.txt`; mọi điểm sử dụng version khác phải đồng bộ.
* [ ] `LATEST.txt` phải cập nhật **CUỐI CÙNG** trong quy trình publish.
* [ ] Nếu dùng `package.zip`, `version.json.package.sha256` và `size` là bắt buộc.
* [ ] Không thay đổi file config quan trọng (`setup.iss`, `installer/version.iss`, biến đường dẫn release root) nếu không được yêu cầu rõ ràng.
* [ ] Không thêm dependency mới nếu không có lý do kỹ thuật bắt buộc.
* [ ] Thêm comment ngắn gọn cho logic phức tạp/nhạy cảm (version parse, rollback, copy/retry).

### Cac quy tac khuyen nghi (soft rules)

* [ ] Ưu tiên giữ logic update thành các hàm nhỏ, dễ test và dễ rollback.
* [ ] Ưu tiên dùng script có sẵn (`build_app.bat`, `publish_release.bat`, `scripts/preflight_update.ps1`) thay vì viết lại thủ công.
* [ ] Ưu tiên **fail-fast**: phát hiện mismatch version/hash sớm trước khi copy lên remote.
* [ ] Ưu tiên **idempotent update**: có thể chạy lại publish script mà không phá release đã tồn tại.

### Cach goi skill (cho nguoi dung)

* **Implicit (tự động):**
    * "Áp dụng skill này để chuẩn hóa quy trình publish update LAN."
    * "Review luồng update hiện tại và tạo checklist trước release."
    * "Sửa script publish để an toàn hơn với `LATEST.txt`."
* **Explicit (bắt buộc dùng skill):**
    * `/skills` -> chọn `update-release-workflow`
    * `$update-release-workflow`
    * `codex skill update-release-workflow`

### Cac tai nguyen phu thuoc

* **Scripts:** `scripts/preflight_update.ps1` (kiểm tra trước build/publish).
* **Tài liệu tham khảo:**
    * `references/guideline.md` (release/update guideline cho LAN workflow).
    * `references/checklist.md` (checklist pre-release, post-release, rollback).
* **Template:** `assets/version.json.template` (manifest mẫu để khởi tạo nhanh version metadata).

### Ghi chu trien khai cho dev

* **Tên skill:** `name` dùng chữ thường + số + dấu gạch ngang (`-`), không bắt đầu/kết thúc bằng `-`, không có `--`. Tên folder phải trùng với giá trị `name`.
* **Giới hạn:** `description` ngắn gọn, đầy đủ trigger, ưu tiên dưới 1024 ký tự. Giữ `SKILL.md` gọn, ưu tiên dưới 500 dòng; nội dung chi tiết đưa sang `references/`.
* **Progressive disclosure:** Chỉ load `references/guideline.md` và `references/checklist.md` khi cần. Không nhân bản thông tin dài dòng giữa `SKILL.md` và reference files.