from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class RequestModel(BaseModel):
    item_id: str
    value: str


@router.post("/example")
async def handle_example(request: RequestModel):
    """
    Template endpoint:
    - validate request with Pydantic
    - run core logic in try block
    - return consistent response shape
    """
    try:
        # Replace this block with real business logic.
        result = {
            "item_id": request.item_id,
            "value": request.value,
            "status": "processed",
        }
        return {"data": result}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Internal error: {exc}")
