from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from excel.engine import load_excel, compare_dataframes

router = APIRouter()

TEMP_DIR = "temp"

class CompareRequest(BaseModel):
    file1: str
    file2: str

@router.post("/compare")
async def compare_files(request: CompareRequest):
    """
    Compare two uploaded Excel files by filename.
    """
    file1_path = os.path.join(TEMP_DIR, request.file1)
    file2_path = os.path.join(TEMP_DIR, request.file2)
    
    if not os.path.exists(file1_path) or not os.path.exists(file2_path):
        raise HTTPException(status_code=404, detail="One or both files not found.")
        
    try:
        df1 = load_excel(file1_path)
        df2 = load_excel(file2_path)
        
        result = compare_dataframes(df1, df2)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")
