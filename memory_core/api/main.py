from fastapi import FastAPI
from models.schema import MemoryRequest, QueryRequest, MemoryResponse, QueryResponse
from services.embeddings import generate_embedding
from services.vector_store import init_collection, insert_vector, search_vectors
from services.memory_store import insert_memory, fetch_memories_by_ids
from services.groq_client import generate_answer

app = FastAPI()

init_collection()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/memory", response_model=MemoryResponse)
def add_memory(request: MemoryRequest):
    embedding = generate_embedding(request.text)
    memory_id = insert_memory(request.text)
    insert_vector(memory_id, embedding)
    return MemoryResponse(message="Memory stored successfully", memory_id=memory_id)

@app.post("/query", response_model=QueryResponse)
def query_memory(request: QueryRequest):
    embedding = generate_embedding(request.query)
    memory_ids = search_vectors(embedding)
    memories = fetch_memories_by_ids(memory_ids)
    answer = generate_answer(memories, request.query)
    return QueryResponse(top_memories=memories, answer=answer)