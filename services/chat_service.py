from dataclasses import dataclass

from langchain_classic.memory import ConversationBufferMemory

from agents.executors import crear_agente_consultar, crear_agente_crear
from agents.router import router_con_memoria
from services.memory import PersistentMemoryManager

INSTRUCCIONES_CONTEXTO = {
    "crear": "Revisa el contexto anterior para extraer nombre y email si ya fueron mencionados.",
    "consultar": "Revisa el contexto anterior para entender qué información busca el usuario.",
}

AGENTES = {
    "crear": crear_agente_crear,
    "consultar": crear_agente_consultar,
}

MENSAJE_NO_ENTENDIDO = "❓ No entendí la solicitud. Por favor, reformula tu mensaje."


@dataclass
class ChatResult:
    respuesta: str
    session_id: str
    decision: str


def _resumir_contexto(memory: ConversationBufferMemory) -> list[str]:
    lineas = []
    for msg in memory.chat_memory.messages[:-1]:
        if msg.type == "human":
            lineas.append(f"Usuario dijo: {msg.content}")
        else:
            lineas.append(f"Asistente respondió: {msg.content}")
    return lineas


def enriquecer_mensaje(
    mensaje: str,
    memory: ConversationBufferMemory,
    decision: str,
) -> str:
    contexto = _resumir_contexto(memory)
    if not contexto:
        return mensaje

    instruccion = INSTRUCCIONES_CONTEXTO[decision]
    historial = "\n".join(contexto)
    return (
        f"Contexto de la conversación anterior:\n"
        f"{historial}\n"
        f"Mensaje actual del usuario: {mensaje}\n"
        f"IMPORTANTE: {instruccion}"
    )


def ejecutar_agente(
    decision: str,
    mensaje: str,
    memory: ConversationBufferMemory,
) -> str:
    factory = AGENTES.get(decision)
    if not factory:
        return MENSAJE_NO_ENTENDIDO

    mensaje_con_contexto = enriquecer_mensaje(mensaje, memory, decision)
    try:
        agente = factory(memory)
        resultado = agente.invoke({"input": mensaje_con_contexto})
        return resultado.get("output", str(resultado))
    except Exception as e:
        return f"❌ Error en agente {decision}: {str(e)}"


def procesar_mensaje(session_id: str, mensaje: str) -> ChatResult:
    memory = PersistentMemoryManager.load_memory_for_agent(session_id)
    PersistentMemoryManager.save_message(
        session_id=session_id,
        role="user",
        content=mensaje,
    )

    try:
        decision = router_con_memoria(mensaje, memory)
    except Exception as e:
        respuesta = f"❌ Error al procesar la solicitud: {str(e)}"
        PersistentMemoryManager.save_message(
            session_id=session_id,
            role="assistant",
            content=respuesta,
        )
        return ChatResult(
            respuesta=respuesta,
            session_id=session_id,
            decision="error",
        )

    memory.chat_memory.add_user_message(mensaje)

    if decision in AGENTES:
        respuesta = ejecutar_agente(decision, mensaje, memory)
    else:
        decision = "desconocido"
        respuesta = MENSAJE_NO_ENTENDIDO

    PersistentMemoryManager.save_message(
        session_id=session_id,
        role="assistant",
        content=respuesta,
    )

    return ChatResult(
        respuesta=respuesta,
        session_id=session_id,
        decision=decision,
    )
