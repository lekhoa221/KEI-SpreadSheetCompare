# Guideline điều phối Checklist và Backlog

## Mục tiêu

Giữ mọi phiên làm việc đi qua một nguồn sự thật duy nhất: `Checklist & backlog.md`.

## Luật vận hành cốt lõi

1. Không có file SSOT thì không làm task.
2. Nếu file chưa tồn tại:
   - Tạo file từ template.
   - Dừng tại bước xác nhận với user.
3. Chỉ được bắt đầu sửa code sau khi task đã được ghi vào checklist hoặc backlog.
4. Mọi thay đổi trạng thái phải đi kèm một dòng lịch sử.

## Phân loại nhiệm vụ

- Vào `Checklist chính`:
  - Tính năng chính.
  - Luồng phát triển cốt lõi.
  - Danh sách thành phần trong bộ skill.
- Vào `Backlog phụ trợ`:
  - Debug.
  - Tinh chỉnh nhẹ.
  - Việc linh tinh ngoài luồng chính.

## Trạng thái chuẩn

- `TODO`: chưa bắt đầu.
- `DOING`: đang xử lý.
- `DONE`: hoàn tất.
- `BLOCKED`: bị chặn, cần làm rõ.

## Chuẩn ghi lịch sử

Mẫu khuyến nghị:

`YYYY-MM-DD HH:mm:ss | CHECKLIST hoặc BACKLOG | Mã việc | Trạng thái | Mô tả ngắn`

Ví dụ:

`2026-02-09 15:10:00 | CHECKLIST | CL-003 | DOING | Bắt đầu tách logic update manager`
