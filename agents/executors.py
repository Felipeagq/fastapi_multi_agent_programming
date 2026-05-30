from langchain_classic.agents import AgentType, initialize_agent
from langchain_classic.memory import ConversationBufferMemory

from agents.tools import consultar_clientes, crear_cliente
from core.llm import llm

PREFIX_CREAR = """
Eres un agente que SOLO crea clientes.

IMPORTANTE: Antes de preguntar información, REVISA EL HISTORIAL DE LA CONVERSACIÓN.
El usuario puede haber proporcionado el nombre o email en mensajes anteriores.

Proceso:
1. Revisa el historial completo de la conversación
2. Extrae el nombre si ya fue mencionado
3. Extrae el email si ya fue mencionado
4. Si tienes AMBOS (nombre Y email), ejecuta la herramienta crear_cliente
5. Si falta alguno, pregunta SOLO por lo que falta

NO repitas preguntas que ya fueron respondidas en el historial.
"""

PREFIX_CONSULTAR = """
Eres un agente que SOLO consulta información de clientes.

IMPORTANTE: Revisa el historial de la conversación para entender el contexto completo.
El usuario puede estar refinando o filtrando una consulta anterior.

Proceso:
1. Revisa el historial para entender qué información busca el usuario
2. Utiliza la herramienta consultar_clientes para obtener la lista
3. Si el usuario pidió un filtro específico, aplica ese filtro a los resultados
4. Presenta la información de forma clara y organizada
"""


def _build_agent(
    tools: list,
    prefix: str,
    memory: ConversationBufferMemory | None = None,
):
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        memory=memory,
        agent_kwargs={"prefix": prefix},
    )


def crear_agente_crear(memory: ConversationBufferMemory | None = None):
    return _build_agent([crear_cliente], PREFIX_CREAR, memory=memory)


def crear_agente_consultar(memory: ConversationBufferMemory | None = None):
    return _build_agent([consultar_clientes], PREFIX_CONSULTAR, memory=memory)
