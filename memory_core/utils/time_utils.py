from datetime import datetime, timezone

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def days_since(dt: datetime) -> float:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    delta = now_utc() - dt
    return delta.total_seconds() / 86400