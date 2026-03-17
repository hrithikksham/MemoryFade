from services.embeddings import generate_embedding
from services.vector_store import search_vectors_with_scores
from services.memory_store import fetch_memories_by_ids, update_memory_access
from services.decay_engine import apply_decay_to_all
from config.settings import SIMILARITY_THRESHOLD, TOP_K, TOP_N


def retrieve_and_update(query: str):
    apply_decay_to_all()

    embedding = generate_embedding(query)


    # Step 2: search vectors
    hits = search_vectors_with_scores(embedding, top_k=TOP_K)

    if not hits:
        return []

    filtered_hits = [
        hit for hit in hits
        if hit.score >= SIMILARITY_THRESHOLD
        ]

    if not filtered_hits and hits:
    # take best match anyway
        filtered_hits = [hits[0]]

    # Step 4: sort by score (descending)
    ranked_hits = sorted(filtered_hits, key=lambda x: x.score, reverse=True)

    # Step 5: select top N
    selected_hits = ranked_hits[:TOP_N]

    # Step 6: extract memory IDs
    memory_ids = [hit.payload["memory_id"] for hit in selected_hits]

    # Step 7: fetch memory data
    memories = [m for m in memories if m["state"] != "ARCHIVED"]
    memories = fetch_memories_by_ids(memory_ids)

    # Step 8: reinforce ONLY selected memories
    for mem in memories:
        update_memory_access(mem["id"])

    return memories