import pandas as pd
import os

def get_sheet_names(file_path):
    """Return a list of sheet names in the Excel file."""
    try:
        xl = pd.ExcelFile(file_path, engine='openpyxl')
        return xl.sheet_names
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {str(e)}")

def get_sheet_data(file_path, sheet_name):
    """
    Return the content of a sheet as JSON-friendly list of lists (grid),
    handling NaN and converting types for frontend display.
    """
    try:
        # Load raw data without header inference to get everything as grid
        df = pd.read_excel(file_path, sheet_name=sheet_name, header=None, engine='openpyxl')
        
        # Replace NaN with empty string
        df = df.fillna("")
        
        # Convert to list of lists
        data = df.values.tolist()
        
        return {
            "rows": len(data),
            "cols": len(data[0]) if data else 0,
            "data": data
        }
    except Exception as e:
        raise ValueError(f"Error reading sheet data: {str(e)}")
