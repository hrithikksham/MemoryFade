from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
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

def insert_vector(memory_id: str, embedding: list[float]):
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=memory_id,
                vector=embedding,
                payload={"memory_id": memory_id}
            )
        ]
    )

def search_vectors_with_scores(embedding: list[float], top_k: int = 5):
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=embedding,
        limit=top_k
    ).points

    return results