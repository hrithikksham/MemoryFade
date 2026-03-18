from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct, Filter, FieldCondition, MatchValue
from config.settings import QDRANT_HOST, QDRANT_PORT

COLLECTION_NAME = "memories"
VECTOR_SIZE = 384

client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)


def init_collection():
    existing = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
        )


def insert_vector(memory_id: str, embedding: list[float], user_id: str):
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=memory_id,
                vector=embedding,
                payload={
                    "memory_id": memory_id,
                    "user_id": user_id   # ✅ CRITICAL
                }
            )
        ]
    )


def search_vectors_with_scores(embedding: list[float], user_id: str, top_k: int = 5):
    results = client.query_points(
        collection_name=COLLECTION_NAME,
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