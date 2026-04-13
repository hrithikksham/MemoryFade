from datetime import datetime
from utils.time_utils import now_utc, days_since
from services.memory_store import get_all_memories, update_memory_fields


def compute_decay(memory: dict) -> float:
    now = now_utc()

    last_decay = memory.get("last_decay_run", memory["last_accessed"])
    last_accessed = memory["last_accessed"]

    if isinstance(last_decay, str):
        last_decay = datetime.fromisoformat(last_decay.replace("Z", "+00:00"))
    if isinstance(last_accessed, str):
        last_accessed = datetime.fromisoformat(last_accessed.replace("Z", "+00:00"))

    # Use whichever is older as the decay baseline
    baseline = min(last_decay, last_accessed)

    delta = now - baseline
    days = delta.total_seconds() / 86400

    print(f"[DEBUG] Days since decay baseline: {days:.2f}")

    # Grace period — no decay within 2 days
    if days < 2:
        return memory["strength"]

    decay = round(days * 2, 2)
    new_strength = max(memory["strength"] - decay, 0)

    return new_strength


def compute_state(memory: dict, new_strength: float) -> str:
    days_since_access = days_since(memory["last_accessed"])
    access_count = memory["access_count"]

    # Hard decay conditions checked FIRST — override everything
    if new_strength <= 0:
        return "ARCHIVED"

    if new_strength < 20 and days_since_access > 14:
        return "ARCHIVED"

    if new_strength < 40 or days_since_access > 7:
        return "FADING"

    # ACTIVE only applies to genuinely recent, healthy memories
    if access_count >= 3 and days_since_access < 7 and new_strength >= 40:
        return "ACTIVE"

    return "FRESH"


def apply_decay_to_user(user_id: str):
    memories = get_all_memories(user_id)

    for memory in memories:

        if memory["state"] == "ARCHIVED":
            continue

        new_strength = compute_decay(memory)
        new_state = compute_state(memory, new_strength)

        print(
            f"[DECAY] {memory['text'][:30]}... | "
            f"{memory['strength']} → {new_strength} | {new_state}"
        )

        update_memory_fields(
            memory_id=memory["id"],
            user_id=user_id,
            strength=new_strength,
            state=new_state,
            last_decay_run=now_utc().isoformat()
        )