from datetime import datetime, timezone
from services.memory_store import get_all_memories, update_memory_fields


def compute_decay(memory):
    now = datetime.now(timezone.utc)

    last_decay = memory.get("last_decay_run", memory["last_accessed"])

    if isinstance(last_decay, str):
        last_decay = datetime.fromisoformat(last_decay.replace("Z", "+00:00"))

    delta = now - last_decay
    days = delta.total_seconds() / 86400

    # ❗ Only decay if enough time passed
    if days < 1:
        return memory["strength"]  # skip

    decay = round(days * 2, 2)
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
            state=new_state,
            last_decay_run=now_utc().isoformat() # fix needed here
        )

    print(f"[DECAY] {memory['text'][:30]}... | {memory['strength']} → {new_strength} | {new_state}")