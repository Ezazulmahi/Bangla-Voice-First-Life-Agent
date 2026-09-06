from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from agents.registry import register_tool
from models import Reminder, User


@register_tool("set_reminder")
def run(decision, db: Session, user: User) -> tuple[str, dict | None]:
    title = decision.reminder_title or "রিমাইন্ডার"

    due_at = None
    if decision.due_at:
        try:
            due_at = datetime.fromisoformat(decision.due_at)
        except ValueError:
            due_at = None
    if due_at is None:
        due_at = datetime.now(timezone.utc) + timedelta(days=1)

    reminder = Reminder(
        user_id=user.id,
        title=title,
        message=decision.reminder_message,
        due_at=due_at,
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    reply = f"ঠিক আছে, '{title}'-এর জন্য একটি রিমাইন্ডার সেট করা হয়েছে।"
    data = {
        "id": reminder.id,
        "title": reminder.title,
        "due_at": reminder.due_at.isoformat(),
    }
    return reply, data
