# Checklist & Backlog

## ✅ Completed Features
- [x] **Core Engine**: Pandas-based comparison logic.
- [x] **Desktop Migration**: Ported from FastAPI/React to PyQt6.
- [x] **UI Structure**: Side-by-Side Grid View.
- [x] **Dashboard Redesign**: Removed sidebar, added top mode tabs + modern upload card.
- [x] **Synchronization**:
    - [x] Synced Scrolling (Vertical/Horizontal).
    - [x] Synced Cell Selection.
- [x] **Visuals**:
    - [x] Light Theme (Excel-like colors).
    - [x] Custom Card Layout Dashboard.
    - [x] File Type Selector (UI only).
    - [x] Ribbon UI (File/Home/View/Formula/Help tabs).
    - [x] File Metadata Panel (path/size/timestamps/authors/last saved by).
- [x] **Excel Fidelity**:
    - [x] Extract Header/Index correctly (A-Z, 1-N).
    - [x] Extract Background Colors.
    - [x] Extract Font Styles (Bold, Italic, Color, Size).
    - [x] Theme/Indexed Color Support (closer to Excel).
    - [x] Extract Alignment (Left, Right, Center).
    - [x] Support Merged Cells.
- [x] **Excel UX Tools**:
    - [x] Increase/Decrease Decimal (selection-based display).
    - [x] Number Format Parsing (basic).
    - [x] Auto-Fit Columns (manual).
    - [x] Wrap Text Toggle.
    - [x] Copy Selected Range.
- [x] **User Settings**:
    - [x] Config file (last opened directory).
- [x] **Packaging**: `run_desktop.bat` script created.

## 🚧 In Progress / Partially Implemented
- [ ] **Border Rendering**: 
    - *Status*: Basic monochrome borders via `BorderDelegate`.
    - *Next*: Support real Excel border colors + thickness without visual artifacts.

## 📋 Backlog (Future Features)
### v2.1 (Planned)
- [ ] **Word Comparison**: Implement `.docx` text differencing.
- [ ] **PowerPoint Comparison**: Implement `.pptx` slide differencing (image-based or text-based).
- [ ] **Export Report**: Button to export comparison results to a new Excel file (highlighting differences).

### v2.2 (Planned - Excel UX)
- [ ] **Find / Search**: In-grid search with next/prev.

### v2.3 (Planned - Compare Controls)
- [x] **Diff Visibility Toggle**: Show/Hide changes overlay (content diff) [default off].
- [x] **Filter Differences**: Only Changes / Content Only / Format Only / Both.
- [x] **Ignore Options**: Ignore whitespace, case, or number format differences (default off).
- [ ] **Diff Detail Map**:
    - [x] Precompute `diff_map[(row,col)] = {content, format, formula}`.
    - [x] Compare format: fill, font, alignment, border, number_format.
    - [x] Content compare options: strict / normalized (trim, case).
- [ ] **Diff Rendering**:
    - [x] Non-invasive markers (inner border or corner mark).
    - [x] Preserve original cell formatting.
    - [x] Toggleable per type (content vs format).
    - [x] Formula diff marker.

### v3.0 (Long Term)
- [ ] **Advanced Filtering**: Filter rows to show "Only Changes".
- [ ] **Formula Engine**: Compare formulas instead of just values.
- [ ] **Folder Compare**: Batch comparison of multiple files in a directory.
- .exe Installer (using PyInstaller/InnoSetup).
