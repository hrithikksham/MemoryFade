from utils.time_utils import now_utc
from models.memory_model import MemoryState


# -------------------------------
# IMPORTANCE (CLEAN HEURISTIC)
# -------------------------------
def calculate_importance(text: str) -> float:
    word_count = len(text.split())

    if word_count < 5:
        return 3.0
    elif word_count < 15:
        return 5.0
    else:
        return 7.0


# -------------------------------
# REINFORCEMENT
# -------------------------------
def apply_reinforcement(memory: dict) -> dict:
    memory["strength"] = round(min(memory["strength"] + 5, 100), 2)
    memory["access_count"] += 1
    memory["last_accessed"] = now_utc().isoformat()
    return memory


# -------------------------------
# DECAY
# -------------------------------
def apply_decay(memory: dict) -> dict:
    days = days_since_str(memory["last_accessed"])

    decay = round(days * 2, 2)  # stronger realistic decay
    memory["strength"] = round(max(memory["strength"] - decay, 0), 2)

    return memory


# -------------------------------
# RETENTION (ADVANCED METRIC)
# -------------------------------
def calculate_retention(memory: dict) -> float:
    days_old = days_since_str(memory["created_at"])
    age_factor = days_old * 0.1

    retention = memory["strength"] / (1 + age_factor)

    return round(retention, 2)


# -------------------------------
# STATE LOGIC (FINAL CLEAN)
# -------------------------------
def compute_state(strength: float, access_count: int = 0) -> str:
    if strength < 20:
        return MemoryState.ARCHIVED

    elif strength < 40:
        return MemoryState.FADING

    elif access_count >= 3:
        return MemoryState.ACTIVE

    else:
        return MemoryState.FRESH


# -------------------------------
# UPDATE MEMORY STATE
# -------------------------------
def update_memory_state(memory: dict) -> dict:
    memory["state"] = compute_state(
        memory["strength"],
        memory["access_count"]
    )
    return memory


# -------------------------------
# TIME UTILITY
# -------------------------------
def days_since_str(dt_str) -> float:
    from datetime import datetime, timezone

    if isinstance(dt_str, str):
        dt_str = dt_str.replace("Z", "+00:00")
        dt = datetime.fromisoformat(dt_str)
    else:
        dt = dt_str

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    delta = now_utc() - dt

    return delta.total_seconds() / 86400