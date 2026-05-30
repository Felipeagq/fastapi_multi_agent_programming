from fastapi import APIRouter

from core.schemas import HistoryResponse
from services.memory import PersistentMemoryManager

router = APIRouter(tags=["history"])


@router.get("/history/{session_id}", response_model=HistoryResponse)
async def get_history(session_id: str):
    mensajes = PersistentMemoryManager.get_history(session_id)
    return HistoryResponse(
        session_id=session_id,
        total_mensajes=len(mensajes),
        historial=[
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat(),
            }
            for msg in mensajes
        ],
    )


@router.delete("/history/{session_id}")
async def clear_history(session_id: str):
    PersistentMemoryManager.clear_session(session_id)
    return {
        "message": f"Historial de sesión {session_id} eliminado correctamente",
        "session_id": session_id,
    }
