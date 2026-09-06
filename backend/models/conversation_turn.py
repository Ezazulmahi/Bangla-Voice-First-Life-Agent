import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import relationship

from database import Base


class TurnRole(str, enum.Enum):
    user = "user"
    agent = "agent"


class ToolName(str, enum.Enum):
    mobile_compare = "mobile_compare"
    statement_explain = "statement_explain"
    complaint_draft = "complaint_draft"
    set_reminder = "set_reminder"
    explain_process = "explain_process"


class ConversationTurn(Base):
    __tablename__ = "conversation_turns"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False, index=True)
    role = Column(Enum(TurnRole), nullable=False)
    audio_file_path = Column(String(500), nullable=True)
    transcript_text = Column(Text, nullable=False)
    tool_used = Column(Enum(ToolName), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    conversation = relationship("Conversation", back_populates="turns")
