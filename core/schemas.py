from pydantic import BaseModel


class ChatRequest(BaseModel):
    mensaje: str


class ChatResponse(BaseModel):
    respuesta: str
    session_id: str
    decision: str


class HistoryResponse(BaseModel):
    session_id: str
    total_mensajes: int
    historial: list
