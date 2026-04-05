from services.embeddings import generate_embedding
from services.vector_store import search_vectors_with_scores
from services.memory_store import fetch_memories_by_ids, update_memory_access
from services.decay_engine import apply_decay_to_user
from config.settings import TOP_K, TOP_N
from utils.time_utils import days_since


# ----------------------------------
# FINAL SCORING FUNCTION
# ----------------------------------

def compute_final_score(hit, memory) -> float:
    similarity = getattr(hit, "score", 0.0)

    importance = memory.get("importance", 5) / 10
    strength = memory.get("strength", 50) / 100

    last_accessed = memory.get("last_accessed")
    recency_days = days_since(last_accessed) if last_accessed else 0
    recency_score = max(0, 1 - (recency_days / 30))

    state = memory.get("state", "FRESH")
    state_penalty = {
        "ARCHIVED": 0.25,
        "FADING": 0.75
    }.get(state, 1.0)

    final_score = (
        0.55 * similarity +
        0.15 * importance +
        0.20 * strength +
        0.10 * recency_score
    ) * state_penalty

    return final_score


# ----------------------------------
# MAIN RETRIEVAL PIPELINE
# ----------------------------------

def retrieve_and_update(
    query: str,
    user_id: str,
    embedding_model: str = "mxbai" 
) -> list:

    # 1. Apply decay before retrieval
    apply_decay_to_user(user_id)

    # 2. Normalize query
    query = query.strip().lower()

    # 3. Generate embedding
    embedding = generate_embedding(query, model_name=embedding_model)

    # 4. Vector search — fixed: keyword arg is model_name not embedding_model
    hits = search_vectors_with_scores(
        embedding,
        user_id=user_id,
        top_k=TOP_K,
        model_name=embedding_model
    )

    if not hits:
        return []

    print("\n--- VECTOR HITS ---")
    for hit in hits:
        print(
            "ID:", hit.payload["memory_id"],
            "SIM:", round(getattr(hit, "score", 0), 3)
        )

    # 5. Fetch memories from Supabase
    memory_ids = [hit.payload["memory_id"] for hit in hits]
    memories = fetch_memories_by_ids(memory_ids, user_id)

    if not memories:
        return []

    memory_map = {m["id"]: m for m in memories}

    # 6. Score each hit
    scored_memories = []
    for hit in hits:
        mem_id = hit.payload["memory_id"]
        if mem_id not in memory_map:
            continue
        memory = memory_map[mem_id]
        score = compute_final_score(hit, memory)
        scored_memories.append((memory, score))

    if not scored_memories:
        return []

    # 7. Rank by final score
    ranked = sorted(scored_memories, key=lambda x: x[1], reverse=True)

    print("\n--- FINAL RANKING ---")
    for mem, score in ranked[:TOP_N]:
        print(mem["id"], mem["state"], round(score, 3))

    # 8. Select top N
    top_memories = [memory for memory, _ in ranked[:TOP_N]]

    # 9. Reinforcement — boost accessed memories
    for memory in top_memories:
        update_memory_access(memory["id"], user_id)

    return top_memories