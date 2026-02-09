---
name: desktop-pyqt-ui-implementation
description: |
  Trien khai va review desktop UI PyQt cho project Spreadsheet Compare theo quy trinh ro rang (startup flow, main window layout, result grid interaction, signal-slot wiring, verification). Dung khi nguoi dung yeu cau tao moi/sua/refactor/review giao dien desktop trong `ui/` hoac `desktop_app.py`, xu ly responsiveness cua widget, hoac toi uu luong thao tac ma khong pha vo logic hien tai. Khong dung cho frontend React, backend API, hoac release deployment workflow.
---

# Desktop PyQt UI Implementation

### Muc dich cua skill

- Muc tieu chinh cua skill nay la chuyen yeu cau giao dien desktop thanh thay doi PyQt co cau truc ro rang, de test, va de maintain.
- Skill giup giam loi thao tac UI, giam regressions o luong compare, va giu code nhat quan giua `desktop_app.py`, `ui/main_window.py`, va `ui/excel/result_view.py`.

### Khi nao dung skill nay?

- Dieu kien 1: Khi nguoi dung yeu cau tao widget moi, sua layout, refactor signal-slot, hoac review giao dien desktop.
- Dieu kien 2: Khi pham vi task nam trong `desktop_app.py`, `ui/`, hoac cac module core duoc desktop UI goi truc tiep.
- Khong dung: Khi task thuoc frontend React, backend FastAPI, hoac luong publish update release.

### Quy trinh hoat dong (step-by-step)

1. **Phan tich yeu cau**
   - Xac dinh yeu cau la:
     - [ ] Tao moi
     - [ ] Sua / refactor
     - [ ] Review / kiem tra
     - [ ] Khac
   - Lam ro scope: startup, dashboard, upload flow, compare flow, result view, hoac feedback and update prompt.
   - Doc context toi thieu:
     - `desktop_app.py`
     - `ui/main_window.py`
     - `ui/file_drop.py`
     - `ui/excel/result_view.py`

2. **Chuan bi / dieu kien**
   - Xac dinh stack:
     - PyQt6 widgets + signal and slot
     - qdarktheme light theme
     - WorkerThread cho tac vu nang de tranh block UI thread
   - Chay preflight:
     - `powershell -ExecutionPolicy Bypass -File .skills/desktop-pyqt-ui-implementation/scripts/preflight_desktop_ui.ps1 -ProjectRoot .`
   - Neu can verify chat che:
     - `powershell -ExecutionPolicy Bypass -File .skills/desktop-pyqt-ui-implementation/scripts/preflight_desktop_ui.ps1 -ProjectRoot . -VerifyQtImports -RunCompile`

3. **Thuc hien tac vu chinh**
   - Tuan thu quy tac trong `references/guideline.md`.
   - Neu tao widget moi:
     - Dung template `assets/pyqt-widget-template.py`.
   - Uu tien thay doi toi thieu can thiet, giu hanh vi hien tai va contract signal.
   - Neu can chay thu nhanh:
     - `run_desktop.bat`

4. **Kiem tra / toi uu**
   - Dung checklist trong `references/checklist.md`.
   - Kiem tra:
     - loading and error states
     - responsiveness khi resize window
     - dong bo state giua MainWindow va ResultView
     - khong co long-running task trong main thread.

### Cac quy tac bat buoc (hard rules)

- [ ] Frontmatter chi gom `name` va `description`.
- [ ] Khong block UI thread bang thao tac nang; phai dung QThread hoac co che async phu hop.
- [ ] Khong pha vo luong signal-slot hien tai neu khong co yeu cau ro rang.
- [ ] Khong doi path loading asset cho bundle mode (ho tro `sys._MEIPASS`) neu chua duoc yeu cau.
- [ ] Khong sua backend API hay frontend React trong task desktop UI neu khong duoc chi dinh.
- [ ] Khong them dependency moi neu stack hien tai dap ung.
- [ ] Them comment ngan gon cho logic phuc tap (sync selection, filter, formula parsing, update flow).

### Cac quy tac khuyen nghi (soft rules)

- [ ] Uu tien tach ham nho trong MainWindow and ResultView de de review.
- [ ] Uu tien naming ro nghia cho widget, action, va signal.
- [ ] Uu tien cap nhat style qua objectName va central stylesheet thay vi style inline qua nhieu.
- [ ] Uu tien fail-safe UI: loi phai co thong bao ro rang cho user.

### Cach goi skill (cho nguoi dung)

- **Implicit (tu dong):**
  - "Ap dung skill nay de sua giao dien desktop PyQt cho man hinh ket qua."
  - "Review `ui/main_window.py` theo guideline cua skill."
  - "Refactor signal-slot cua ResultView de de bao tri hon."

- **Explicit (buoc dung skill):**
  - `/skills` -> chon `desktop-pyqt-ui-implementation`
  - `$desktop-pyqt-ui-implementation`
  - `codex skill desktop-pyqt-ui-implementation`

### Cac tai nguyen phu thuoc

- Scripts:
  - `scripts/preflight_desktop_ui.ps1` - preflight check truoc khi sua hoac review desktop UI.

- Tai lieu tham khao:
  - `references/guideline.md` - guideline desktop PyQt implementation.
  - `references/checklist.md` - checklist review and verification.

- Template:
  - `assets/pyqt-widget-template.py` - khung widget PyQt voi loading and error state.

### Ghi chu trien khai cho dev

- Ten skill:
  - `name` dung chu thuong + so + dau gach ngang.
  - Ten folder trung voi gia tri `name`.

- Gioi han:
  - `description` ngan gon, ro trigger, uu tien duoi 1024 ky tu.
  - `SKILL.md` giu gon, uu tien duoi 500 dong; noi dung chi tiet dua sang `references/`.

- Progressive disclosure:
  - Chi load `references/guideline.md` va `references/checklist.md` khi can.
  - Khong lap lai noi dung dai dong giua `SKILL.md` va references.
