from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.ai import generate_analysis

router = APIRouter()

class AnalyzeRequest(BaseModel):
    summary: dict
    changes: list

@router.post("/analyze")
async def analyze_changes(request: AnalyzeRequest):
    """
    Analyze the comparison result using AI.
    """
    try:
        explanation = generate_analysis(request.changes, request.summary)
        return {"analysis": explanation}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
