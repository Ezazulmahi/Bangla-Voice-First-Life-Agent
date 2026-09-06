from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from agents.registry import register_tool
from models import Reminder, User
from utils.timezone import BD_TZ


@register_tool("set_reminder")
def run(decision, db: Session, user: User) -> tuple[str, dict | None]:
    lang = user.preferred_language.value
    default_title = {"bn": "রিমাইন্ডার", "en": "Reminder"}
    title = decision.reminder_title or default_title[lang]

    due_at = None
    if decision.due_at:
        try:
            due_at = datetime.fromisoformat(decision.due_at)
        except ValueError:
            due_at = None
    if due_at is None:
        due_at = datetime.now(BD_TZ) + timedelta(days=1)

    reminder = Reminder(
        user_id=user.id,
        title=title,
        message=decision.reminder_message,
        due_at=due_at,
    )
    db.add(reminder)
    db.commit()
    db.refresh(reminder)

    reply_templates = {
        "bn": f"ঠিক আছে, '{title}'-এর জন্য একটি রিমাইন্ডার সেট করা হয়েছে।",
        "en": f"Done — I've set a reminder for '{title}'.",
    }
    reply = reply_templates[lang]
    data = {
        "id": reminder.id,
        "title": reminder.title,
        "due_at": reminder.due_at.isoformat(),
    }
    return reply, data
