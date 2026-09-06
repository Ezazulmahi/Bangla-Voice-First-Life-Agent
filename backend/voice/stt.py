from groq import Groq

from config import settings

_client: Groq | None = None


def _get_client() -> Groq:
    global _client
    if not settings.groq_api_key:
        raise RuntimeError("GROQ_API_KEY is not set — speech-to-text is unavailable.")
    if _client is None:
        _client = Groq(api_key=settings.groq_api_key)
    return _client


def transcribe(audio_bytes: bytes, filename: str = "audio.webm") -> str:
    """Transcribe Bangla speech using Groq's hosted Whisper model."""
    client = _get_client()
    result = client.audio.transcriptions.create(
        file=(filename, audio_bytes),
        model=settings.groq_stt_model,
        language="bn",
    )
    return result.text.strip()
