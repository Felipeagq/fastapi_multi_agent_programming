from langchain.tools import tool

from core.database import SessionLocal
from core.models import Cliente


@tool
def crear_cliente(nombre: str, email: str) -> str:
    """Crea un cliente en la base de datos. Requiere nombre y email."""
    db = SessionLocal()
    try:
        cliente = Cliente(nombre=nombre, email=email)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return f"✅ Cliente creado: {cliente.nombre} ({cliente.email})"
    except Exception as e:
        db.rollback()
        return f"❌ Error: {str(e)}"
    finally:
        db.close()


@tool
def consultar_clientes() -> str:
    """Devuelve la lista de todos los clientes registrados."""
    db = SessionLocal()
    try:
        clientes = db.query(Cliente).all()
        if not clientes:
            return "📭 No hay clientes registrados"
        return "\n".join(f"- {c.nombre} | {c.email}" for c in clientes)
    finally:
        db.close()
