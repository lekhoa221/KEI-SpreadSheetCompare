---
name: frontend-ui-implementation
description: |
  Trien khai va review giao dien frontend cho project React + Vite + Tailwind theo quy trinh co kiem soat (phan tich yeu cau, xac dinh state/API contract, implementation theo component, verification lint/build). Dung khi nguoi dung yeu cau tao moi/sua/refactor/review UI, xu ly responsive, hoac toi uu trai nghiem va kha nang bao tri ma khong pha vo workflow hien tai. Khong dung cho backend API logic, desktop PyQt UI, hoac thay doi ha tang deploy.
---

# Frontend UI Implementation

### Muc dich cua skill

- Muc tieu chinh cua skill nay la chuyen yeu cau giao dien thanh thay doi code frontend ro rang, co test, va de review.
- Skill giup tiet kiem thoi gian thong qua quy trinh + checklist + preflight script de giam loi khi chinh sua UI.

### Khi nao dung skill nay?

- Dieu kien 1: Khi nguoi dung yeu cau tao man hinh moi, sua layout, refactor component, hoac review UI theo guideline.
- Dieu kien 2: Khi project dung React 18 + Vite + Tailwind trong thu muc `frontend/`.
- Khong dung: Khi task thuoc backend Python/FastAPI, desktop PyQt (`ui/`), hoac release/update deployment flow.

### Quy trinh hoat dong (step-by-step)

1. **Phan tich yeu cau**
   - Xac dinh yeu cau la:
     - [ ] Tao moi
     - [ ] Sua / refactor
     - [ ] Review / kiem tra
     - [ ] Khac
   - Lam ro scope man hinh, state, event, API endpoint, va responsive target.
   - Doc context toi thieu:
     - `frontend/src/App.jsx`
     - `frontend/src/components/*.jsx`
     - `frontend/vite.config.js`
     - `frontend/src/index.css`

2. **Chuan bi / dieu kien**
   - Xac dinh stack:
     - React 18 (hooks + functional component)
     - Vite 7
     - TailwindCSS 3
     - Axios API calls qua `/api` proxy
   - Chay preflight:
     - `powershell -ExecutionPolicy Bypass -File .skills/frontend-ui-implementation/scripts/preflight_frontend.ps1 -ProjectRoot .`
   - Neu can verify chat che:
     - `powershell -ExecutionPolicy Bypass -File .skills/frontend-ui-implementation/scripts/preflight_frontend.ps1 -ProjectRoot . -RunLint -RunBuild`

3. **Thuc hien tac vu chinh**
   - Tuan thu quy tac trong `references/guideline.md`.
   - Khi tao component moi:
     - Dung `assets/component-template.jsx` lam base.
   - Uu tien thay doi toi thieu can thiet, giu ten file va structure nhat quan voi code hien co.
   - Neu co API interaction:
     - Giu contract endpoint (`/api/upload`, `/api/compare`, `/api/sheets/...`, `/api/data/...`) neu chua co yeu cau doi backend.

4. **Kiem tra / toi uu**
   - Dung checklist trong `references/checklist.md`.
   - Bat buoc check lint/build truoc khi ket thuc task UI lon.
   - Review lai:
     - logic loading/error state
     - responsive desktop/mobile
     - readability va maintainability component.

### Cac quy tac bat buoc (hard rules)

- [ ] Frontmatter chi gom `name` va `description`.
- [ ] Khong doi API contract frontend-backend neu khong duoc yeu cau ro rang.
- [ ] Khong them dependency moi neu co the giai quyet bang stack hien tai.
- [ ] Khong sua cac file release/update script (`build_app.bat`, `publish_release.bat`) trong task frontend.
- [ ] Luon giu loading + error state cho thao tac bat dong bo (upload, compare, fetch data).
- [ ] Neu logic component phuc tap, them comment ngan gon o diem can thiet.

### Cac quy tac khuyen nghi (soft rules)

- [ ] Uu tien tach component nho theo trach nhiem don le.
- [ ] Uu tien class util ro rang va nhat quan mau sac/spacing.
- [ ] Uu tien reusable helper cho xu ly state va transform data.
- [ ] Uu tien layout responsive tu dau, khong de den cuoi moi fix mobile.

### Cach goi skill (cho nguoi dung)

- **Implicit (tu dong):**
  - "Ap dung skill nay de tao man hinh compare moi cho frontend."
  - "Review component UploadZone theo guideline cua skill."
  - "Refactor SxSView de de bao tri hon va van giu UX hien tai."

- **Explicit (buoc dung skill):**
  - `/skills` -> chon `frontend-ui-implementation`
  - `$frontend-ui-implementation`
  - `codex skill frontend-ui-implementation`

### Cac tai nguyen phu thuoc

- Scripts:
  - `scripts/preflight_frontend.ps1` - kiem tra dieu kien frontend truoc implementation/review.

- Tai lieu tham khao:
  - `references/guideline.md` - guideline code/UI architecture cho frontend.
  - `references/checklist.md` - checklist review va verify truoc ban giao.

- Template:
  - `assets/component-template.jsx` - khung component co loading/error/content state.

### Ghi chu trien khai cho dev

- Ten skill:
  - `name` dung chu thuong + so + dau gach ngang.
  - Ten folder trung voi gia tri `name`.

- Gioi han:
  - `description` ro trigger, ngan gon, uu tien duoi 1024 ky tu.
  - `SKILL.md` giu gon, uu tien duoi 500 dong; dua chi tiet sang `references/`.

- Progressive disclosure:
  - Chi load `references/guideline.md` hoac `references/checklist.md` khi can.
  - Khong lap lai noi dung dai dong giua `SKILL.md` va references.
