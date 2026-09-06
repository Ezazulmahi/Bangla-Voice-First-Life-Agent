from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from database import get_db
from deps import get_current_user
from models import Reminder, User
from schemas.reminder import ReminderIn, ReminderOut, ReminderUpdate

router = APIRouter(prefix="/reminders", tags=["reminders"])


def _get_owned_reminder(reminder_id: int, user: User, db: Session) -> Reminder:
    reminder = db.get(Reminder, reminder_id)
    if reminder is None or reminder.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Reminder not found")
    return reminder


@router.post("", response_model=ReminderOut)
def create_reminder(
    payload: ReminderIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reminder = Reminder(user_id=current_user.id, **payload.model_dump())
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    return reminder


@router.get("", response_model=list[ReminderOut])
def list_reminders(
    q: str | None = Query(default=None, description="filter by title/message substring"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Reminder).filter(Reminder.user_id == current_user.id)
    if q:
        like = f"%{q}%"
        query = query.filter((Reminder.title.ilike(like)) | (Reminder.message.ilike(like)))
    return query.order_by(Reminder.due_at.asc()).limit(limit).offset(offset).all()


@router.patch("/{reminder_id}", response_model=ReminderOut)
def update_reminder(
    reminder_id: int,
    payload: ReminderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reminder = _get_owned_reminder(reminder_id, current_user, db)
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(reminder, field, value)
    if "due_at" in updates or updates.get("enabled") is True:
        # A pushed-back due date, or re-enabling a reminder, should be able
        # to notify again.
        reminder.notified_at = None
    db.commit()
    db.refresh(reminder)
    return reminder


@router.delete("/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reminder(
    reminder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reminder = _get_owned_reminder(reminder_id, current_user, db)
    db.delete(reminder)
    db.commit()
