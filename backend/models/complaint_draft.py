from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func

from database import Base


class ComplaintDraft(Base):
    __tablename__ = "complaint_drafts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    conversation_turn_id = Column(
        Integer, ForeignKey("conversation_turns.id", ondelete="SET NULL"), nullable=True
    )
    company_name = Column(String(200), nullable=False)
    issue_description = Column(Text, nullable=False)
    generated_text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
