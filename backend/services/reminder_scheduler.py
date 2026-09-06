import logging
from datetime import datetime, timezone

from apscheduler.schedulers.background import BackgroundScheduler

from config import settings
from database import SessionLocal
from models import PushSubscription, Reminder
from services.push import PushSubscriptionExpired, send_push

logger = logging.getLogger("sohai.reminders")

_scheduler: BackgroundScheduler | None = None


def check_due_reminders() -> None:
    if not settings.vapid_private_key:
        return  # push not configured — nothing to do

    db = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        due = (
            db.query(Reminder)
            .filter(Reminder.enabled.is_(True), Reminder.notified_at.is_(None), Reminder.due_at <= now)
            .all()
        )
        for reminder in due:
            subs = db.query(PushSubscription).filter(PushSubscription.user_id == reminder.user_id).all()
            for sub in subs:
                try:
                    send_push(sub, reminder.title, reminder.message or "Sohai reminder · সোহাই রিমাইন্ডার")
                except PushSubscriptionExpired:
                    db.delete(sub)
                except Exception:
                    logger.exception("push send failed for reminder %s", reminder.id)
            reminder.notified_at = now
        db.commit()
    finally:
        db.close()


def start_scheduler() -> None:
    global _scheduler
    if _scheduler is not None:
        return
    _scheduler = BackgroundScheduler(daemon=True)
    _scheduler.add_job(
        check_due_reminders,
        "interval",
        seconds=settings.reminder_poll_seconds,
        id="check_due_reminders",
    )
    _scheduler.start()


def stop_scheduler() -> None:
    global _scheduler
    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None
