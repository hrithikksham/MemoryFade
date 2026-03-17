from supabase import create_client
from config.settings import SUPABASE_URL, SUPABASE_KEY
from utils.time_utils import now_utc
from services.memory_engine import compute_state

client = create_client(SUPABASE_URL, SUPABASE_KEY)


def insert_memory(text: str, importance: float) -> str:
    now = now_utc().isoformat()

    strength = max(min(importance * 10, 100), 20)  # safe initial range

    response = client.table("memories").insert({
        "text": text,
        "importance": importance,
        "strength": strength,
        "last_accessed": now,
        "access_count": 0,
        "state": "FRESH"
    }).execute()

    return response.data[0]["id"]



def fetch_memories_by_ids(ids: list[str]) -> list[dict]:
    if not ids:
        return []

    response = client.table("memories").select("*").in_("id", ids).execute()
    id_to_row = {row["id"]: row for row in response.data}

    return [id_to_row[id] for id in ids if id in id_to_row]



def update_memory_access(memory_id: str):
    response = client.table("memories").select("*").eq("id", memory_id).execute()

    if not response.data:
        return

    memory = response.data[0]

    # Reinforcement
    new_strength = min(memory["strength"] + 5, 100)
    new_access_count = memory["access_count"] + 1

    new_state = compute_state(new_strength, new_access_count)

    client.table("memories").update({
        "strength": new_strength,
        "access_count": new_access_count,
        "last_accessed": now_utc().isoformat(),
        "state": new_state
    }).eq("id", memory_id).execute()



def update_memory(memory_id: str, fields: dict):
    client.table("memories").update(fields).eq("id", memory_id).execute()



def get_all_memories():
    response = client.table("memories").select("*").execute()
    return response.data

def update_memory_fields(memory_id: str, strength: float, state: str):
    client.table("memories").update({
        "strength": strength,
        "state": state
    }).eq("id", memory_id).execute()