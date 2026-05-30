from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.database import Base, engine
from routes.chat import router as chat_router
from routes.history import router as history_router
from routes.meta import router as meta_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Sistema Multi-Agente con Memoria Persistente",
        description="API REST para gestión de clientes con agentes conversacionales y memoria por sesiones",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    Base.metadata.create_all(bind=engine)

    app.include_router(meta_router)
    app.include_router(chat_router)
    app.include_router(history_router)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    from config import API_HOST, API_PORT

    uvicorn.run(
        "entrypoint:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
    )
