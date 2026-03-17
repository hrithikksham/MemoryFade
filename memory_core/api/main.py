from fastapi import FastAPI
from models.schema import MemoryRequest, QueryRequest, MemoryResponse, QueryResponse
from services.embeddings import generate_embedding
from services.vector_store import init_collection, insert_vector
from services.memory_store import insert_memory
from services.memory_engine import calculate_importance
from services.retrieval import retrieve_and_update
from services.groq_client import generate_answer

app = FastAPI()

init_collection()


@app.post("/memory", response_model=MemoryResponse)
def add_memory(request: MemoryRequest):
    importance = calculate_importance(request.text)
    embedding = generate_embedding(request.text)
    memory_id = insert_memory(request.text, importance)
    insert_vector(memory_id, embedding)

    return MemoryResponse(
        message="Memory stored successfully",
        memory_id=memory_id,
        importance=importance
    )


@app.post("/query", response_model=QueryResponse)
def query_memory(request: QueryRequest):

    memories = retrieve_and_update(request.query)

    if not memories:
        return QueryResponse(
            top_memories=[],
            answer="No memory found for this query."
        )

    texts = [m["text"] for m in memories]

    answer = generate_answer(texts, request.query)

    return QueryResponse(
        top_memories=texts,
        answer=answer
    )

@app.get("/memory/{memory_id}")
def get_memory(memory_id: str):
    from services.memory_store import fetch_memories_by_ids
    results = fetch_memories_by_ids([memory_id])
    if not results:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Memory not found")
    return results[0]