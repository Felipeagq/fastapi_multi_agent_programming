import uuid
from typing import Optional

from fastapi import APIRouter, Header

from core.schemas import ChatRequest, ChatResponse
from services.chat_service import procesar_mensaje

router = APIRouter(tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    session_id: Optional[str] = Header(None, alias="session-id"),
):
    session_id = session_id or str(uuid.uuid4())
    result = procesar_mensaje(session_id, request.mensaje)
    return ChatResponse(
        respuesta=result.respuesta,
        session_id=result.session_id,
        decision=result.decision,
    )
