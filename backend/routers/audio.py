import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from agents.router_agent import route
from config import settings
from database import get_db
from deps import get_current_user
from models import ConversationTurn, TurnRole, User
from routers.conversations import get_owned_conversation
from schemas.conversation import AudioTurnResult
from voice import stt, tts

router = APIRouter(prefix="/conversations", tags=["audio"])


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

    transcript = stt.transcribe(audio_bytes, filename=audio.filename or "audio.webm")

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

    result = route(transcript, current_user, db)
    reply_audio_url = tts.synthesize(result.reply_text)

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
