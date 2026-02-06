import pandas as pd
import os

def get_sheet_names(file_path):
    """Return a list of sheet names in the Excel file."""
    try:
        xl = pd.ExcelFile(file_path, engine='openpyxl')
        return xl.sheet_names
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {str(e)}")

import openpyxl

def get_sheet_data(file_path, sheet_name):
    """
    Return the content of a sheet and its formatting metadata.
    """
    try:
        # Load data first (Keeping pandas for robustness/consistency if needed, 
        # but we also need openpyxl for dimensions)
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, engine='openpyxl')
        df = df.fillna("")
        data = df.values.tolist()
        
        # Load formatting via openpyxl
        wb = openpyxl.load_workbook(file_path, data_only=True, read_only=False) # read_only doesn't support dim?
        ws = wb[sheet_name]
        
        col_widths = {}
        row_heights = {}
        
        # Extract Column Widths
        # OpenPyXL column dimensions are 1-indexed (A, B, C...)
        # We need to map them to 0-indexed integers
        for col_char, dim in ws.column_dimensions.items():
            if dim.width:
                # Approximate conversion: Excel width units to Pixels
                # Factor is roughly ~7-8 pixels per unit depending on font.
                # Standard conversion: (Width * 7) roughly?
                # PyQt expects pixels. Let's try separate logic in UI or approximate here.
                # A generic approximation: width * 7 + 10 padding
                col_idx = openpyxl.utils.cell.column_index_from_string(col_char) - 1
                col_widths[col_idx] = dim.width
            
        # Extract Row Heights
        for row_idx, dim in ws.row_dimensions.items():
            if dim.height:
                # OpenPyXL uses points for height? Or pixels?
                # Usually points. 1 point = 1.33 px roughly.
                row_heights[row_idx - 1] = dim.height

        wb.close()
        
        return {
            "rows": len(data),
            "cols": len(data[0]) if data else 0,
            "data": data,
            "col_widths": col_widths,
            "row_heights": row_heights
        }
    except Exception as e:
        raise ValueError(f"Error reading sheet data: {str(e)}")
