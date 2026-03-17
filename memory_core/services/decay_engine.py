from datetime import datetime, timezone
from services.memory_store import get_all_memories, update_memory_fields


def compute_decay(memory):
    now = datetime.now(timezone.utc)

    last_accessed = memory["last_accessed"]
    if isinstance(last_accessed, str):
        last_accessed = datetime.fromisoformat(last_accessed.replace("Z", "+00:00"))

    days = (now - last_accessed).days

    # Decay formula
    decay = days * 2  # simple linear decay
    new_strength = max(memory["strength"] - decay, 0)

    return new_strength


def compute_state(strength, access_count):
    if strength > 70 and access_count > 3:
        return "ACTIVE"
    elif strength > 30:
        return "FADING"
    else:
        return "ARCHIVED"


def apply_decay_to_all():
    memories = get_all_memories()

    for memory in memories:
        new_strength = compute_decay(memory)
        new_state = compute_state(new_strength, memory["access_count"])

        update_memory_fields(
            memory_id=memory["id"],
            strength=new_strength,
            state=new_state
        )

    print(f"[DECAY] {memory['text'][:30]}... | {memory['strength']} → {new_strength} | {new_state}")