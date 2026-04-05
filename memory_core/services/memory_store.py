from supabase import create_client
from config.settings import SUPABASE_URL, SUPABASE_KEY
from utils.time_utils import now_utc
from services.memory_engine import compute_state


client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ---------------------------------
# INSERT MEMORY
# ---------------------------------

def insert_memory(
    text: str,
    importance: float,
    user_id: str,
    embedding_model: str = "mxbai-embed-large"
) -> str:
    now = now_utc().isoformat()
    strength = max(min(importance * 10, 100), 30)
    state = compute_state(strength, 0)

    response = (
        client
        .table("memories")
        .insert({
            "user_id": user_id,
            "text": text,
            "importance": importance,
            "strength": strength,
            "access_count": 0,
            "state": state,
            "embedding_model": embedding_model,
            "created_at": now,
            "last_accessed": now,
            "last_decay_run": now
        })
        .execute()
    )

    return response.data[0]["id"]


# ---------------------------------
# FETCH MEMORIES
# ---------------------------------

def fetch_memories_by_ids(
    ids: list[str],
    user_id: str
) -> list[dict]:
    if not ids:
        return []

    response = (
        client
        .table("memories")
        .select("*")
        .in_("id", ids)
        .eq("user_id", user_id)
        .execute()
    )

    id_map = {row["id"]: row for row in response.data}

    return [id_map[id] for id in ids if id in id_map]


# ---------------------------------
# UPDATE ACCESS
# ---------------------------------

def update_memory_access(
    memory_id: str,
    user_id: str
):
    response = (
        client
        .table("memories")
        .select("*")
        .eq("id", memory_id)
        .eq("user_id", user_id)
        .execute()
    )

    if not response.data:
        return

    memory = response.data[0]

    new_strength = min(memory["strength"] + 6, 100)
    new_access_count = memory["access_count"] + 1
    new_state = compute_state(new_strength, new_access_count)

    (
        client
        .table("memories")
        .update({
            "strength": new_strength,
            "access_count": new_access_count,
            "last_accessed": now_utc().isoformat(),
            "state": new_state
        })
        .eq("id", memory_id)
        .eq("user_id", user_id)
        .execute()
    )


# ---------------------------------
# GET ALL MEMORIES
# ---------------------------------

def get_all_memories(user_id: str) -> list[dict]:
    response = (
        client
        .table("memories")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    return response.data


# ---------------------------------
# UPDATE DECAY
# ---------------------------------

def update_memory_fields(
    memory_id: str,
    user_id: str,
    strength: float,
    state: str,
    last_decay_run: str
):
    (
        client
        .table("memories")
        .update({
            "strength": strength,
            "state": state,
            "last_decay_run": last_decay_run
        })
        .eq("id", memory_id)
        .eq("user_id", user_id)
        .execute()
    )