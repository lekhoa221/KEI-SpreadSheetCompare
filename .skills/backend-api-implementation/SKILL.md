---
name: backend-api-implementation
description: |
  Trien khai va review backend API cho project FastAPI cua Spreadsheet Compare theo quy trinh ro rang (router design, validation, error handling, integration voi core modules, verification). Dung khi nguoi dung yeu cau tao moi/sua/refactor/review endpoint API, xu ly upload/compare/sheets/analyze flow, hoac chuan hoa contract giua frontend va backend. Khong dung cho frontend UI implementation, desktop PyQt UI, hoac release deployment workflow.
---

# Backend API Implementation

### Muc dich cua skill

- Muc tieu chinh cua skill nay la bien yeu cau API thanh thay doi backend FastAPI co cau truc ro rang, an toan va de bao tri.
- Skill giup giam loi contract frontend-backend, giam regressions trong upload and compare flow, va tang toc do review nhung van giu chat luong.

### Khi nao dung skill nay?

- Dieu kien 1: Khi nguoi dung yeu cau tao endpoint moi, sua router, refactor service logic, hoac review backend.
- Dieu kien 2: Khi project dang dung FastAPI voi cau truc `backend/main.py`, `backend/routers`, `backend/core`.
- Khong dung: Khi task chu yeu la frontend React, desktop PyQt, hoac publish update release.

### Quy trinh hoat dong (step-by-step)

1. **Phan tich yeu cau**
   - Xac dinh yeu cau la:
     - [ ] Tao moi
     - [ ] Sua / refactor
     - [ ] Review / kiem tra
     - [ ] Khac
   - Lam ro endpoint nao bi anh huong, request and response schema, va business logic can doi.
   - Doc context toi thieu:
     - `backend/main.py`
     - `backend/routers/*.py`
     - `backend/core/*.py`
     - `backend/requirements.txt`

2. **Chuan bi / dieu kien**
   - Xac dinh stack:
     - FastAPI + Uvicorn
     - Pydantic models cho request validation
     - Pandas and OpenPyXL cho xu ly Excel
     - Ollama cho AI analysis endpoint
   - Chay preflight:
     - `powershell -ExecutionPolicy Bypass -File .skills/backend-api-implementation/scripts/preflight_backend.ps1 -ProjectRoot .`
   - Neu can verify sau khi sua lon:
     - `powershell -ExecutionPolicy Bypass -File .skills/backend-api-implementation/scripts/preflight_backend.ps1 -ProjectRoot . -RunCompile -RunPytest`

3. **Thuc hien tac vu chinh**
   - Tuan thu quy tac trong `references/guideline.md`.
   - Uu tien dat logic HTTP trong router va logic xu ly du lieu trong `backend/core`.
   - Bao toan contract endpoint hien co neu chua duoc yeu cau thay doi:
     - `POST /api/upload`
     - `POST /api/compare`
     - `GET /api/sheets/{filename}`
     - `GET /api/data/{filename}/{sheet_name}`
     - `POST /api/analyze`
   - Neu tao endpoint moi:
     - Dung template `assets/router-template.py`.

4. **Kiem tra / toi uu**
   - Dung checklist trong `references/checklist.md`.
   - Kiem tra xu ly loi:
     - file khong ton tai
     - payload sai format
     - loi I and O
     - loi service phu thuoc (vd Ollama)
   - Dam bao ma tra ve va thong diep loi de frontend xu ly on dinh.

### Cac quy tac bat buoc (hard rules)

- [ ] Frontmatter chi gom `name` va `description`.
- [ ] Khong pha vo contract API hien tai neu khong co yeu cau ro rang.
- [ ] Khong bo qua validation request cho endpoint ghi du lieu.
- [ ] Khong swallow exception im lang; phai map sang HTTPException hop ly.
- [ ] Khong them dependency moi neu stack hien tai da dap ung.
- [ ] Khong sua build and publish scripts trong task backend API neu khong duoc yeu cau.
- [ ] Them comment ngan gon neu logic phuc tap khong tu mo ta.

### Cac quy tac khuyen nghi (soft rules)

- [ ] Uu tien tach ham nho va thu nghiem duoc trong `backend/core`.
- [ ] Uu tien naming ro nghia cho routers, models, va helper functions.
- [ ] Uu tien fail-fast va thong diep loi nhat quan.
- [ ] Uu tien giu response shape co tinh on dinh cho frontend.

### Cach goi skill (cho nguoi dung)

- **Implicit (tu dong):**
  - "Ap dung skill nay de tao endpoint backend moi."
  - "Review routers trong backend theo guideline cua skill."
  - "Refactor luong compare API de de maintain hon."

- **Explicit (buoc dung skill):**
  - `/skills` -> chon `backend-api-implementation`
  - `$backend-api-implementation`
  - `codex skill backend-api-implementation`

### Cac tai nguyen phu thuoc

- Scripts:
  - `scripts/preflight_backend.ps1` - preflight check truoc khi sua hoac review backend.

- Tai lieu tham khao:
  - `references/guideline.md` - guideline backend API implementation.
  - `references/checklist.md` - checklist truoc khi ban giao.

- Template:
  - `assets/router-template.py` - khung router FastAPI voi request model va error handling.

### Ghi chu trien khai cho dev

- Ten skill:
  - `name` dung chu thuong + so + dau gach ngang.
  - Ten folder trung voi gia tri `name`.

- Gioi han:
  - `description` ngan gon, ro trigger, uu tien duoi 1024 ky tu.
  - `SKILL.md` giu gon, uu tien duoi 500 dong; dua chi tiet sang `references/`.

- Progressive disclosure:
  - Chi load `references/guideline.md` hoac `references/checklist.md` khi can.
  - Khong lap lai noi dung dai dong giua `SKILL.md` va references.
