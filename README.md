# Sistema Multi-Agente con Memoria Persistente

API REST con FastAPI, LangChain y SQLAlchemy.

## Estructura

```
├── app_factory.py       # Arranque y app FastAPI
├── config.py            # Variables de entorno
├── core/                # Infraestructura compartida
│   ├── database.py
│   ├── models.py
│   ├── llm.py
│   └── schemas.py       # Contratos API (Pydantic)
├── agents/              # LangChain: router, ejecutores, tools
│   ├── router.py
│   ├── executors.py
│   └── tools.py
├── services/            # Lógica de negocio
│   ├── chat_service.py
│   └── memory.py
├── routes/              # Endpoints HTTP
└── requirements.txt
```

## Instalación

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Uso

```bash
python app_factory.py
# o
uvicorn app_factory:app --reload --port 8004
```

Docs: http://localhost:8004/docs

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Info de la API |
| GET | `/health` | Estado |
| POST | `/chat` | Chat (header opcional `session-id`) |
| GET | `/history/{session_id}` | Historial |
| DELETE | `/history/{session_id}` | Borrar historial |

Ver `.env.example` para `OPENAI_API_KEY` y puerto.
