from supabase import create_client
from config.settings import SUPABASE_URL, SUPABASE_KEY

client = create_client(SUPABASE_URL, SUPABASE_KEY)

def insert_memory(text: str) -> str:
    response = client.table("memories").insert({"text": text}).execute()
    return response.data[0]["id"]

def fetch_memories_by_ids(ids: list[str]) -> list[str]:
    response = client.table("memories").select("id, text").in_("id", ids).execute()
    id_to_text = {row["id"]: row["text"] for row in response.data}
    return [id_to_text[id] for id in ids if id in id_to_text]