import enum

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, func

from database import Base


class NotifyChannel(str, enum.Enum):
    app = "app"
    sms = "sms"


class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    message = Column(String(500), nullable=True)
    due_at = Column(DateTime(timezone=True), nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    notify_channel = Column(Enum(NotifyChannel), nullable=False, default=NotifyChannel.app)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
