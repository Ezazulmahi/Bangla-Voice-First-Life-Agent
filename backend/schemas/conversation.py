from datetime import datetime

from pydantic import BaseModel


class ConversationOut(BaseModel):
    id: int
    created_at: datetime
    last_transcript: str | None = None
    last_tool_used: str | None = None

    class Config:
        from_attributes = True


class ConversationTurnOut(BaseModel):
    id: int
    role: str
    transcript_text: str
    audio_file_path: str | None
    tool_used: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class AudioTurnResult(BaseModel):
    transcript: str
    reply_text: str
    reply_audio_url: str | None
    tool_used: str | None
    data: dict | None
