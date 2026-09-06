from datetime import datetime

from pydantic import BaseModel


class ReminderIn(BaseModel):
    title: str
    message: str | None = None
    due_at: datetime


class ReminderUpdate(BaseModel):
    title: str | None = None
    message: str | None = None
    due_at: datetime | None = None
    enabled: bool | None = None


class ReminderOut(BaseModel):
    id: int
    title: str
    message: str | None
    due_at: datetime
    enabled: bool
    notify_channel: str
    created_at: datetime

    class Config:
        from_attributes = True
