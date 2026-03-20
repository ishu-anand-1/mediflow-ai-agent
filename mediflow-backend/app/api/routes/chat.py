from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas.domain import ChatRequest, ChatResponse
from app.services.agent import chat_with_agent

router = APIRouter()

@router.post("", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, db: AsyncSession = Depends(get_db)):
    reply_dict = await chat_with_agent(request.session_id, request.message, db)
    return ChatResponse(message=reply_dict["message"], data=reply_dict.get("data", {}))
