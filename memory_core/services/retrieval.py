from services.embeddings import generate_embedding
from services.vector_store import search_vectors_with_scores
from services.memory_store import fetch_memories_by_ids, update_memory_access
from services.decay_engine import apply_decay_to_user
from config.settings import TOP_K, TOP_N
from utils.time_utils import days_since


def compute_final_score(hit, memory):
    """
    Production-grade scoring function
    """

    # -----------------------------
    # Core Signals
    # -----------------------------
    similarity = getattr(hit, "score", 0.0)

    importance = memory.get("importance", 0)
    strength = memory.get("strength", 0) / 100

    # safer datetime handling
    last_accessed = memory.get("last_accessed")
    recency_days = days_since(last_accessed) if last_accessed else 0

    # normalize recency (0 → recent, 1 → old)
    recency_score = max(0, 1 - (recency_days / 30))

    # -----------------------------
    # State penalty (IMPORTANT FIX)
    # -----------------------------
    state = memory.get("state", "FRESH")

    state_penalty = 1.0
    if state == "ARCHIVED":
        state_penalty = 0.2   # instead of removing → penalize
    elif state == "FADING":
        state_penalty = 0.7

    # -----------------------------
    # Final Weighted Score
    # -----------------------------
    score = (
        0.5 * similarity +
        0.2 * importance +
        0.2 * strength +
        0.1 * recency_score
    ) * state_penalty

    return score


def retrieve_and_update(query: str, user_id: str):
    # -----------------------------
    # Step 1: Apply decay
    # -----------------------------
    apply_decay_to_user(user_id)

    # -----------------------------
    # Step 2: Normalize query
    # -----------------------------
    query = query.strip().lower()

    # -----------------------------
    # Step 3: Generate embedding
    # -----------------------------
    embedding = generate_embedding(query)

    # -----------------------------
    # Step 4: Vector search
    # -----------------------------
    hits = search_vectors_with_scores(
        embedding,
        user_id=user_id,
        top_k=TOP_K
    )

    if not hits:
        return []

    # -----------------------------
    # DEBUG (keep for now)
    # -----------------------------
    print("\n--- VECTOR HITS ---")
    for hit in hits:
        print("ID:", hit.payload["memory_id"], "SCORE:", getattr(hit, "score", 0))

    # -----------------------------
    # Step 5: Extract IDs
    # -----------------------------
    memory_ids = [hit.payload["memory_id"] for hit in hits]

    if not memory_ids:
        return []

    # -----------------------------
    # Step 6: Fetch DB memories
    # -----------------------------
    memories = fetch_memories_by_ids(memory_ids, user_id)

    if not memories:
        return []

    # -----------------------------
    # Step 7: Map memories
    # -----------------------------
    memory_map = {m["id"]: m for m in memories}

    # -----------------------------
    # Step 8: Compute scores
    # -----------------------------
    scored = []

    for hit in hits:
        mem_id = hit.payload["memory_id"]

        if mem_id not in memory_map:
            continue

        memory = memory_map[mem_id]

        final_score = compute_final_score(hit, memory)

        scored.append((memory, final_score))

    if not scored:
        return []

    # -----------------------------
    # Step 9: Sort
    # -----------------------------
    ranked = sorted(
        scored,
        key=lambda x: x[1],
        reverse=True
    )

    # -----------------------------
    # Step 10: Select Top N
    # -----------------------------
    top_memories = [m for m, _ in ranked[:TOP_N]]

    # -----------------------------
    # Step 11: Reinforcement
    # -----------------------------
    for mem in top_memories:
        update_memory_access(mem["id"], user_id)

    return top_memories