import os
import tempfile
import pandas as pd

def convert_xls_to_xlsx(xls_path):
    """
    Convert an .xls file to a temporary .xlsx file using pandas.
    Returns the path to the temporary .xlsx file, or None if conversion failed.
    """
    if not os.path.exists(xls_path):
        return None
        
    try:
        # Create temp file
        fd, temp_path = tempfile.mkstemp(suffix=".xlsx")
        os.close(fd)
        
        # Read all sheets from .xls
        # xlrd is required for reading .xls
        xls = pd.ExcelFile(xls_path, engine="xlrd")
        
        # Write to .xlsx using openpyxl (default for xlsx)
        with pd.ExcelWriter(temp_path, engine="openpyxl") as writer:
            for sheet_name in xls.sheet_names:
                df = pd.read_excel(xls, sheet_name=sheet_name)
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
        return temp_path
    except Exception as e:
        print(f"XLS Conversion Error: {e}")
        return None
