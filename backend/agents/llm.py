from langchain_groq import ChatGroq

from config import settings

_llm: ChatGroq | None = None


def get_llm(temperature: float = 0.3) -> ChatGroq:
    if not settings.groq_api_key:
        raise RuntimeError("GROQ_API_KEY is not set — the agent/LLM is unavailable.")
    global _llm
    if _llm is None:
        _llm = ChatGroq(
            api_key=settings.groq_api_key,
            model=settings.groq_llm_model,
            temperature=temperature,
        )
    return _llm
