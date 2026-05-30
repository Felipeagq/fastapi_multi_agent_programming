from fastapi import APIRouter

router = APIRouter(tags=["meta"])


@router.get("/")
async def root():
    return {
        "message": "API Multi-Agente con Memoria Persistente",
        "version": "1.0.0",
    }


@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "Sistema Multi-Agente",
        "database": "connected",
    }
