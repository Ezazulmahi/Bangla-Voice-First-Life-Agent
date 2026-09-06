import uuid
from pathlib import Path

from gtts import gTTS

from config import settings


def synthesize(text: str, lang: str = "bn") -> str | None:
    """Synthesize speech (in the given language) and return a media-relative
    URL, or None if synthesis failed (callers should degrade to text-only
    rather than error).

    gTTS (a free wrapper around Google Translate's TTS endpoint) is a
    pragmatic stand-in for a production Bangla voice (e.g. Coqui TTS or a
    paid cloud TTS API) — it needs no API key and has a usable Bangla voice,
    which keeps the MVP demoable end-to-end without extra provisioning.
    """
    if not text.strip():
        return None
    try:
        media_dir = Path(settings.media_dir)
        media_dir.mkdir(parents=True, exist_ok=True)
        filename = f"{uuid.uuid4().hex}.mp3"
        path = media_dir / filename
        gTTS(text=text, lang=lang).save(str(path))
        return f"/media/{filename}"
    except Exception:
        return None
