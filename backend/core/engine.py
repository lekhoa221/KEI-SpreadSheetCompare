import pandas as pd
import numpy as np


def load_excel(file_path):
    """Load an Excel file into a Pandas DataFrame."""
    try:
        # Load the first sheet by default for now
        # Use header=None to treat all rows as data (coordinate-based comparison)
        df = pd.read_excel(file_path, sheet_name=0, header=None, engine='openpyxl')
        return df
    except Exception as e:
        raise ValueError(f"Error loading file: {str(e)}")

def compare_dataframes(df_old: pd.DataFrame, df_new: pd.DataFrame):
    """
    Compare two DataFrames and return a summary of changes.
    """
    # 1. Align Columns (by index since we don't have headers)
    max_cols = max(df_old.shape[1], df_new.shape[1])
    
    # Reindex columns to ensure matching shape
    df_old = df_old.reindex(columns=range(max_cols))
    df_new = df_new.reindex(columns=range(max_cols))
    
    # 2. Align Rows
    max_rows = max(len(df_old), len(df_new))
    df_old = df_old.reindex(index=range(max_rows))
    df_new = df_new.reindex(index=range(max_rows))

    changes = []
    
    # 3. Iterate and Compare cell-by-cell
    # Fill NaN with a placeholder
    df_old_filled = df_old.fillna("###NULL###")
    df_new_filled = df_new.fillna("###NULL###")
    
    diff_mask = (df_old_filled != df_new_filled)
    
    # Get coordinates of differences
    diff_locations = np.where(diff_mask)
    rows = diff_locations[0]
    cols = diff_locations[1]
    
    for r, c in zip(rows, cols):
        old_val = df_old.iloc[r, c]
        new_val = df_new.iloc[r, c]
        
        changes.append({
            "row": int(r),
            "col": int(c),
            "old": str(old_val) if pd.notna(old_val) else "",
            "new": str(new_val) if pd.notna(new_val) else "",
            "type": "modified"
        })

    # Summary Stats
    summary = {
        "total_rows": int(max_rows),
        "total_cols": int(max_cols),
        "changes_count": len(changes)
    }

    return {
        "changes": changes,
        "summary": summary
    }
