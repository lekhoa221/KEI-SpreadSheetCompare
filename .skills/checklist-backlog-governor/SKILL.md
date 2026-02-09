---
name: checklist-backlog-governor
description: |
  Điều phối quy trình làm việc bằng một nguồn sự thật duy nhất là file Checklist & backlog.md. Dùng khi cần quản trị tiến độ nhiệm vụ, bắt buộc ghi nhận và cập nhật trạng thái trước khi thực thi task, phân loại đúng checklist chính và backlog phụ trợ, và lưu lịch sử từng bước bằng tiếng Việt. Không dùng để bỏ qua quy trình hoặc xử lý code domain cụ thể khi chưa hoàn tất bước cập nhật checklist.
---

# Checklist Backlog Governor

### Mục đích của skill

- Thiết lập và cưỡng chế quy trình làm việc có kiểm soát bằng một file duy nhất `Checklist & backlog.md`.
- Bảo đảm mọi task đều có dấu vết: được ghi nhận, cập nhật trạng thái, và lưu lịch sử thay đổi theo từng bước.

### Khi nào dùng skill này?

- Khi cần điều phối tiến độ công việc xuyên suốt dự án.
- Khi cần kiểm soát việc AI Agent chỉ thực thi task sau khi đã cập nhật checklist.
- Khi cần phân loại rõ việc chính vào checklist và việc phụ trợ vào backlog.
- Không dùng khi muốn bỏ qua quy trình ghi nhận trạng thái hoặc làm việc ad-hoc không theo kiểm soát.

### Quy trình hoạt động (step-by-step)

1. **Gate SSOT bắt buộc**
   - Luôn chạy script:
     - `powershell -ExecutionPolicy Bypass -File .skills/checklist-backlog-governor/scripts/ensure_checklist_backlog.ps1 -ProjectRoot .`
   - Nếu chưa có `Checklist & backlog.md`:
     - Xem là dự án mới.
     - Chỉ được tạo file này từ template.
     - Prompt đầu tiên phải dừng tại đây và yêu cầu user xem lại, xác nhận.

2. **Ghi nhận yêu cầu trước khi làm**
   - Thêm task vào `Checklist chính` nếu là luồng phát triển cốt lõi.
   - Thêm task vào `Backlog phụ trợ` nếu là debug, tinh chỉnh nhẹ, việc linh tinh.
   - Cập nhật trạng thái ban đầu (`TODO` hoặc `DOING`) trước khi sửa code.

3. **Thực thi có cập nhật trạng thái**
   - Mỗi bước thực thi phải cập nhật trạng thái trong file SSOT.
   - Với mỗi thay đổi trạng thái, bắt buộc thêm một dòng vào `Lịch sử thay đổi`.
   - Có thể dùng script:
     - `powershell -ExecutionPolicy Bypass -File .skills/checklist-backlog-governor/scripts/log_history.ps1 -ProjectRoot . -Entry "..." -Bucket "CHECKLIST" -StepId "CL-001" -Status "DOING"`

4. **Kết thúc task**
   - Đánh dấu `DONE` hoặc `BLOCKED`.
   - Ghi lý do ngắn gọn bằng tiếng Việt dễ hiểu.
   - Đảm bảo user chỉ cần mở đúng `Checklist & backlog.md` là theo dõi được toàn bộ luồng.

### Các quy tắc bắt buộc (hard rules)

- [ ] `Checklist & backlog.md` là SSOT duy nhất cho tiến độ công việc.
- [ ] Không được thực hiện task nếu chưa ghi nhận vào checklist hoặc backlog.
- [ ] Mọi thay đổi trạng thái đều phải có lịch sử thay đổi đi kèm.
- [ ] Nội dung trong file SSOT dùng tiếng Việt ngắn gọn, dễ hiểu.
- [ ] Luồng phát triển chính và danh sách thành phần bộ skill phải nằm trong `Checklist chính`.
- [ ] Việc phụ trợ, debug, tinh chỉnh nhẹ phải vào `Backlog phụ trợ`.

### Các quy tắc khuyến nghị (soft rules)

- [ ] Dùng mã công việc ổn định như `CL-001`, `BL-001` để dễ truy vết.
- [ ] Câu mô tả nhiệm vụ một dòng, tập trung vào kết quả cần đạt.
- [ ] Ưu tiên cập nhật trạng thái theo nhịp nhỏ, tránh dồn cập nhật cuối phiên.

### Cách gọi skill (cho người dùng)

- **Implicit (tự động):**
  - "Dùng quy trình checklist để điều phối task cho dự án này."
  - "Cập nhật backlog và lịch sử trước khi làm phần này."

- **Explicit (buộc dùng skill):**
  - `/skills` -> chọn `checklist-backlog-governor`
  - `$checklist-backlog-governor`
  - `codex skill checklist-backlog-governor`

### Các tài nguyên phụ thuộc

- Scripts:
  - `scripts/ensure_checklist_backlog.ps1` - kiểm tra hoặc khởi tạo file SSOT bắt buộc.
  - `scripts/log_history.ps1` - ghi nhanh một dòng vào lịch sử thay đổi.

- Tài liệu tham khảo:
  - `references/guideline.md` - nguyên tắc điều phối và phân loại checklist, backlog.
  - `references/checklist.md` - checklist vận hành bắt buộc mỗi phiên làm việc.

- Template:
  - `assets/checklist-backlog.template.md` - mẫu chuẩn cho `Checklist & backlog.md`.

### Ghi chú triển khai cho dev

- Tên skill:
  - `name` dùng chữ thường, số, và dấu gạch ngang.
  - Tên folder phải trùng với `name`.

- Giới hạn:
  - Giữ `description` rõ trigger và ngắn gọn.
  - Giữ `SKILL.md` tập trung vào quy trình, không lan man.
