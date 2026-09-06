import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from agents.router_agent import RouterResult, route
from config import settings
from database import get_db
from deps import get_current_user
from models import ConversationTurn, TurnRole, User
from routers.conversations import get_owned_conversation
from schemas.conversation import AudioTurnResult
from voice import stt, tts

router = APIRouter(prefix="/conversations", tags=["audio"])

MAX_AUDIO_BYTES = 15 * 1024 * 1024  # ~15MB — generous for a few minutes of voice notes
ALLOWED_AUDIO_EXTENSIONS = {".webm", ".mp3", ".mp4", ".m4a", ".mpeg", ".mpga", ".ogg", ".wav", ".flac"}
MIN_TRANSCRIPT_CHARS = 2

CLARIFY_REPLY = {
    "bn": "দুঃখিত, আপনার কথা ঠিক বুঝতে পারিনি। আরেকটু স্পষ্ট করে আবার বলবেন কি?",
    "en": "Sorry, I didn't quite catch that. Could you say it again a bit more clearly?",
}
AGENT_ERROR_REPLY = {
    "bn": "দুঃখিত, এই মুহূর্তে একটু সমস্যা হচ্ছে। একটু পরে আবার চেষ্টা করুন।",
    "en": "Sorry, something went wrong on our end. Please try again in a moment.",
}


def _validate_audio(audio: UploadFile, audio_bytes: bytes) -> None:
    if len(audio_bytes) == 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Empty audio file")
    if len(audio_bytes) > MAX_AUDIO_BYTES:
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Audio file too large (max 15MB)")

    suffix = Path(audio.filename or "").suffix.lower()
    content_type_ok = bool(audio.content_type) and audio.content_type.startswith("audio/")
    if not content_type_ok and suffix not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Unsupported audio format")


def _save_input_audio(audio_bytes: bytes, suffix: str) -> str:
    media_dir = Path(settings.media_dir)
    media_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex}{suffix}"
    (media_dir / filename).write_bytes(audio_bytes)
    return f"/media/{filename}"


@router.post("/{conversation_id}/audio", response_model=AudioTurnResult)
async def submit_audio(
    conversation_id: int,
    audio: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    conversation = get_owned_conversation(conversation_id, current_user, db)
    audio_bytes = await audio.read()
    _validate_audio(audio, audio_bytes)

    lang = current_user.preferred_language.value

    try:
        transcript = stt.transcribe(
            audio_bytes, filename=audio.filename or "audio.webm", language_hint=lang
        )
    except RuntimeError:
        raise  # missing GROQ_API_KEY — let main.py's handler turn this into a clean 503
    except Exception:
        raise HTTPException(
            status.HTTP_502_BAD_GATEWAY,
            "কণ্ঠ শনাক্ত করা যায়নি (voice recognition failed), আবার চেষ্টা করুন।",
        )

    user_audio_path = None
    if current_user.audio_retention_opt_in:
        suffix = Path(audio.filename or "audio.webm").suffix or ".webm"
        user_audio_path = _save_input_audio(audio_bytes, suffix)

    db.add(
        ConversationTurn(
            conversation_id=conversation.id,
            role=TurnRole.user,
            audio_file_path=user_audio_path,
            transcript_text=transcript,
        )
    )
    db.commit()

    if len(transcript.strip()) < MIN_TRANSCRIPT_CHARS:
        # Silence, noise, or speech Whisper couldn't make out at all — ask
        # the user to repeat rather than routing gibberish to the agent.
        result = RouterResult(tool_used=None, reply_text=CLARIFY_REPLY[lang], data=None)
    else:
        try:
            result = route(transcript, current_user, db)
        except RuntimeError:
            raise  # missing GROQ_API_KEY
        except Exception:
            result = RouterResult(tool_used=None, reply_text=AGENT_ERROR_REPLY[lang], data=None)

    reply_audio_url = tts.synthesize(result.reply_text, lang=lang)

    db.add(
        ConversationTurn(
            conversation_id=conversation.id,
            role=TurnRole.agent,
            audio_file_path=reply_audio_url,
            transcript_text=result.reply_text,
            tool_used=result.tool_used,
        )
    )
    db.commit()

    return AudioTurnResult(
        transcript=transcript,
        reply_text=result.reply_text,
        reply_audio_url=reply_audio_url,
        tool_used=result.tool_used,
        data=result.data,
    )
