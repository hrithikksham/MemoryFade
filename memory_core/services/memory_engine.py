from utils.time_utils import now_utc
from models.memory_model import MemoryState


# ----------------------------------
# IMPORTANCE SCORING
# ----------------------------------
def calculate_importance(text: str) -> float:

    word_count = len(text.split())

    if word_count <= 5:
        return 3.0

    elif word_count <= 20:
        return 5.0

    else:
        return 7.0


# ----------------------------------
# REINFORCEMENT (memory recall boost)
# ----------------------------------
def apply_reinforcement(memory: dict) -> dict:

    boost = 6

    memory["strength"] = min(
        memory["strength"] + boost,
        100
    )

    memory["access_count"] += 1

    memory["last_accessed"] = now_utc().isoformat()

    return update_memory_state(memory)


# ----------------------------------
# DECAY (Ebbinghaus inspired)
# ----------------------------------
def apply_decay(memory: dict) -> dict:

    days = days_since_str(memory["last_accessed"])

    importance = memory.get("importance", 5)

    # slower decay for important memories
    decay_rate = 0.6 + (5 - importance) * 0.05

    decay_amount = days * decay_rate * 2

    memory["strength"] = max(
        memory["strength"] - decay_amount,
        0
    )

    return update_memory_state(memory)


# ----------------------------------
# RETENTION SCORE (used in ranking)
# ----------------------------------
def calculate_retention(memory: dict) -> float:

    days_old = days_since_str(memory["created_at"])

    stability = 1 + (memory["access_count"] * 0.25)

    retention = memory["strength"] * stability / (1 + days_old * 0.15)

    return round(retention, 2)


# ----------------------------------
# MEMORY STATE CLASSIFICATION
# ----------------------------------
def compute_state(
    strength: float,
    access_count: int
) -> str:

    if strength < 20:
        return MemoryState.ARCHIVED

    elif strength < 45:
        return MemoryState.FADING

    elif access_count >= 3:
        return MemoryState.ACTIVE

    else:
        return MemoryState.FRESH


# ----------------------------------
# UPDATE STATE WRAPPER
# ----------------------------------
def update_memory_state(memory: dict) -> dict:

    memory["state"] = compute_state(
        memory["strength"],
        memory["access_count"]
    )

    return memory


# ----------------------------------
# TIME UTILS
# ----------------------------------
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