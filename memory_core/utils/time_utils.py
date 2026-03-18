from datetime import datetime, timezone

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def days_since(dt) -> float:
    """
    Accepts both string and datetime.
    Returns days since given timestamp.
    """

    # ✅ Handle string input
    if isinstance(dt, str):
        dt = dt.replace("Z", "+00:00")
        dt = datetime.fromisoformat(dt)

    # ✅ Ensure timezone
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    delta = now_utc() - dt
    return delta.total_seconds() / 86400