from services.embeddings import generate_embedding
from services.vector_store import search_vectors_with_scores
from services.memory_store import fetch_memories_by_ids, update_memory_access
from services.decay_engine import apply_decay_to_all
from config.settings import SIMILARITY_THRESHOLD, TOP_K, TOP_N


def retrieve_and_update(query: str):
    # Step 1: Apply decay (safe, controlled)
    apply_decay_to_all()

    # Step 2: Generate embedding
    embedding = generate_embedding(query)

    # Step 3: Vector search
    hits = search_vectors_with_scores(embedding, top_k=TOP_K)

    if not hits:
        return []

    # Step 4: Filter by similarity threshold
    filtered_hits = [
        hit for hit in hits
        if hit.score >= SIMILARITY_THRESHOLD
    ]

    # Step 5: Fallback → take best match
    if not filtered_hits:
        filtered_hits = [hits[0]]

    # Step 6: Rank by similarity
    ranked_hits = sorted(filtered_hits, key=lambda x: x.score, reverse=True)

    # Step 7: Take top N
    selected_hits = ranked_hits[:TOP_N]

    # Step 8: Extract IDs
    memory_ids = [hit.payload["memory_id"] for hit in selected_hits]

    if not memory_ids:
        return []

    # Step 9: Fetch memories from DB
    memories = fetch_memories_by_ids(memory_ids)

    if not memories:
        return []

    # Step 10: Remove archived memories
    memories = [m for m in memories if m["state"] != "ARCHIVED"]

    if not memories:
        return []

    # Step 11: Reinforce selected memories
    for mem in memories:
        update_memory_access(mem["id"])

    return memories