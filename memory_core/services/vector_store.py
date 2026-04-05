from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams,
    Distance,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)
from config.settings import QDRANT_HOST, QDRANT_PORT


# -----------------------------
# MODEL → VECTOR SIZE MAP
# uses same short keys as embeddings.py
# -----------------------------

VECTOR_SIZES = {
    "mxbai": 1024,
    "minilm": 384
}

# Map full names → short keys (mirrors embeddings.py aliases)
MODEL_ALIASES = {
    "mxbai-embed-large": "mxbai",
    "mixedbread-ai/mxbai-embed-large-v1": "mxbai",
    "mxbai": "mxbai",
    "all-MiniLM-L6-v2": "minilm",
    "minilm": "minilm"
}


# -----------------------------
# CLIENT
# -----------------------------

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


# -----------------------------
# RESOLVE MODEL NAME
# -----------------------------

def resolve_model(model_name: str) -> str:
    resolved = MODEL_ALIASES.get(model_name)
    if resolved is None:
        raise ValueError(
            f"Unsupported model: {model_name}. "
            f"Valid options: {list(MODEL_ALIASES.keys())}"
        )
    return resolved


# -----------------------------
# COLLECTION NAME HELPER
# -----------------------------

def get_collection_name(model_name: str) -> str:
    resolved = resolve_model(model_name)
    return f"memories_{resolved}"


# -----------------------------
# INIT COLLECTION
# -----------------------------

def init_collection(model_name: str):
    resolved = resolve_model(model_name)
    collection_name = get_collection_name(resolved)
    vector_size = VECTOR_SIZES[resolved]

    existing = [c.name for c in client.get_collections().collections]

    if collection_name not in existing:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )


# -----------------------------
# INSERT VECTOR
# -----------------------------

def insert_vector(
    memory_id: str,
    embedding: list[float],
    user_id: str,
    model_name: str = "mxbai"
):
    resolved = resolve_model(model_name)
    collection_name = get_collection_name(resolved)

    init_collection(resolved)

    client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=memory_id,
                vector=embedding,
                payload={
                    "memory_id": memory_id,
                    "user_id": user_id,
                    "embedding_model": resolved
                }
            )
        ]
    )


# -----------------------------
# SEARCH
# -----------------------------

def search_vectors_with_scores(
    embedding: list[float],
    user_id: str,
    model_name: str = "mxbai",
    top_k: int = 5
) -> list:
    resolved = resolve_model(model_name)
    collection_name = get_collection_name(resolved)

    results = client.query_points(
        collection_name=collection_name,
        query=embedding,
        limit=top_k,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=user_id)
                )
            ]
        )
    ).points

    return results