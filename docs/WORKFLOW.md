# Application Workflow

## 1. Launch Check
- **User Action**: Double clicks `run_desktop.bat` (or `.exe`).
- **System**: 
    - Activates Python virtual environment.
    - Launches `desktop_app.py`.
    - Initializes `QApplication` with specific styles (Light Theme).

## 2. Main Dashboard (Card Layout)
- **User Action**: 
    - Sees a clean dashboard with a Document Type selector (default: Excel).
    - Can switch to Word/PowerPoint (shows "Coming Soon" placeholder).
    - Drags and Drops two Excel files into the respective "Original" and "Modified" zones.
- **System**:
    - Validates file extensions (`.xlsx`, `.xls`).
    - Updates UI to show loaded filenames.
    - Enables "Run Analysis" button when both files are ready.

## 3. Analysis Process
- **User Action**: Clicks "Run Analysis".
- **System**:
    - Disables interaction (showing "Processing...").
    - Spawns a background `WorkerThread`.
    - **Engine (`core/engine.py`)**:
        - Loads Excel files using `openpyxl` (data_only=True) to extract values.
        - Extracts **Styles**: Background color, Font (bold/italic/size/color), Alignment.
        - Extracts **Merged Cells**.
        - Converts data to Pandas DataFrame.
        - Compares DataFrames cell-by-cell (filling NaNs).
        - Generates a change summary (list of differences with coordinates).
    - Returns DataFrames + Styles + Merges + Results to Main Thread.

## 4. Result View (Side-by-Side)
- **System**:
    - Hides Dashboard, shows `ResultView`.
    - Populates two `QTableWidget` grids side-by-side.
    - Applies recovered Styles (bg, font) to cells.
    - Applies Diff Highlights:
        - **Green-ish** background for New File changes.
        - **Red-ish** background for Old File changes.
    - Applies Merged Cells spans.
    - Syncs vertical/horizontal scrolling between grids.
    - Syncs Selection: Clicking a cell in one grid selects the same cell in the other (Dark Blue highlight).

## 5. Iteration
- **User Action**:
    - Can scroll to review changes.
    - Can click "← Back" to return to Dashboard and upload new files.
