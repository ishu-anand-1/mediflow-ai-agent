from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.services.agent_service import run_agent

router = APIRouter()


# 🔥 Request Schema (IMPORTANT)
class ChatRequest(BaseModel):
    user_id: str
    message: str


# 🔥 Response Schema (optional but clean)
class ChatResponse(BaseModel):
    response: dict


# 🔥 MAIN CHAT ENDPOINT
@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        result = run_agent(
            user_id=request.user_id,
            user_input=request.message,
            db=db
        )

        return {
            "response": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chat processing failed: {str(e)}"
        )