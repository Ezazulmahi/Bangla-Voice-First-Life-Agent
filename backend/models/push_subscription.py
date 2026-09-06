from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func

from database import Base


class PushSubscription(Base):
    """A browser's Web Push subscription (from the PushManager API), used to
    deliver reminder nudges even when the app tab is closed."""

    __tablename__ = "push_subscriptions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    endpoint = Column(Text, nullable=False, unique=True)
    p256dh_key = Column(String(255), nullable=False)
    auth_key = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
