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


def transcribe(audio_bytes: bytes, filename: str = "audio.webm", language_hint: str = "bn") -> str:
    """Transcribe speech using Groq's hosted Whisper model.

    `language_hint` anchors Whisper's language ID to the user's stated
    preference (defaulting to Bangla, the product's primary audience).
    Whisper still transcribes embedded foreign words within an utterance
    correctly even with a hint set — dropping the hint entirely for
    "better code-switching support" was tried and rejected: it let Whisper's
    language-ID lock onto English for otherwise-Bangla utterances with a few
    English loanwords, which is the common case here, not the exception.
    """
    client = _get_client()
    result = client.audio.transcriptions.create(
        file=(filename, audio_bytes),
        model=settings.groq_stt_model,
        language=language_hint,
    )
    return result.text.strip()
