from fastapi import APIRouter, HTTPException
import os
from excel.reader import get_sheet_names, get_sheet_data

router = APIRouter()

TEMP_DIR = "temp"

@router.get("/sheets/{filename}")
async def list_sheets(filename: str):
    """
    Get list of sheet names from an uploaded file.
    """
    file_path = os.path.join(TEMP_DIR, filename)
    print(f"DEBUG: Accessing file at {os.path.abspath(file_path)}")
    if not os.path.exists(file_path):
        print(f"DEBUG: File not found at {os.path.abspath(file_path)}")
        raise HTTPException(status_code=404, detail=f"File not found at {os.path.abspath(file_path)}")
        
    try:
        sheets = get_sheet_names(file_path)
        return {"filename": filename, "sheets": sheets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/data/{filename}/{sheet_name}")
async def get_sheet_content(filename: str, sheet_name: str):
    """
    Get full content of a specific sheet.
    """
    file_path = os.path.join(TEMP_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
        
    try:
        content = get_sheet_data(file_path, sheet_name)
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
