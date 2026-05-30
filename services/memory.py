from typing import List

from langchain_classic.memory import ConversationBufferMemory

from core.database import SessionLocal
from core.models import Mensaje


class PersistentMemoryManager:
    @staticmethod
    def save_message(session_id: str, role: str, content: str):
        db = SessionLocal()
        try:
            db.add(Mensaje(session_id=session_id, role=role, content=content))
            db.commit()
        finally:
            db.close()

    @staticmethod
    def get_history(session_id: str) -> List[Mensaje]:
        db = SessionLocal()
        try:
            return (
                db.query(Mensaje)
                .filter(Mensaje.session_id == session_id)
                .order_by(Mensaje.timestamp)
                .all()
            )
        finally:
            db.close()

    @staticmethod
    def load_memory_for_agent(session_id: str) -> ConversationBufferMemory:
        memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
        )
        for msg in PersistentMemoryManager.get_history(session_id):
            if msg.role == "user":
                memory.chat_memory.add_user_message(msg.content)
            elif msg.role == "assistant":
                memory.chat_memory.add_ai_message(msg.content)
        return memory

    @staticmethod
    def clear_session(session_id: str):
        db = SessionLocal()
        try:
            db.query(Mensaje).filter(Mensaje.session_id == session_id).delete()
            db.commit()
        finally:
            db.close()
