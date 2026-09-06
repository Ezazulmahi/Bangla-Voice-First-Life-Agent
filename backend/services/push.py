import json

from pywebpush import WebPushException, webpush

from config import settings
from models import PushSubscription


class PushSubscriptionExpired(Exception):
    """Raised when the push service reports the subscription is gone (the
    user uninstalled/blocked notifications) — caller should delete it."""


def send_push(subscription: PushSubscription, title: str, body: str) -> None:
    if not settings.vapid_private_key:
        raise RuntimeError("VAPID keys are not configured — push notifications are unavailable.")
    try:
        webpush(
            subscription_info={
                "endpoint": subscription.endpoint,
                "keys": {"p256dh": subscription.p256dh_key, "auth": subscription.auth_key},
            },
            data=json.dumps({"title": title, "body": body}),
            vapid_private_key=settings.vapid_private_key,
            vapid_claims={"sub": f"mailto:{settings.vapid_claim_email}"},
        )
    except WebPushException as e:
        status = e.response.status_code if e.response is not None else None
        if status in (404, 410):
            raise PushSubscriptionExpired from e
        raise
