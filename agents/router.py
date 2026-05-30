from langchain_classic.chains import LLMChain
from langchain_classic.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate

from core.llm import llm

_SYSTEM_ROUTER = """Eres un recepcionista de un sistema de gestión de clientes.

Clasifica la intención del usuario en UNA palabra basándote en el contexto de la conversación:

- crear → registrar, agregar, guardar, añadir clientes
- consultar → listar, ver, buscar, mostrar clientes

IMPORTANTE: Considera el historial de la conversación. Si el usuario está proporcionando información adicional sobre una solicitud anterior, mantén la misma intención.

Responde SOLO con una de estas palabras (sin puntuación ni espacios adicionales):
crear
consultar"""

prompt_router_con_historial = ChatPromptTemplate.from_messages([
    ("system", _SYSTEM_ROUTER),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{mensaje}"),
])

prompt_router = PromptTemplate(
    input_variables=["mensaje"],
    template=_SYSTEM_ROUTER + "\n\nMensaje: {mensaje}\n",
)

router_chain = LLMChain(llm=llm, prompt=prompt_router)


def router_con_memoria(mensaje: str, memory) -> str:
    try:
        response = llm.invoke(
            prompt_router_con_historial.format_messages(
                chat_history=memory.chat_memory.messages,
                mensaje=mensaje,
            )
        )
        return response.content.strip().lower()
    except Exception:
        return router_chain.invoke({"mensaje": mensaje})["text"].strip().lower()
