from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
from config.settings import SUPABASE_URL, SUPABASE_KEY
from models.schema import MemoryRequest, QueryRequest, MemoryResponse, QueryResponse
from services.embeddings import generate_embedding
from services.vector_store import init_collection, insert_vector
from services.memory_store import insert_memory, fetch_memories_by_ids, update_memory_fields
from services.memory_engine import calculate_importance, apply_decay, update_memory_state
from services.retrieval import retrieve_and_update
from services.groq_client import generate_answer
from auth.middleware import get_user_id_from_token
from utils.time_utils import now_utc

app = FastAPI(title="Memora API", version="1.0.0")

# CORS — restrict origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_collection("mxbai")

supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)


# ----------------------------------
# ADD MEMORY
# ----------------------------------

@app.post("/memory", response_model=MemoryResponse)
def add_memory(
    request: MemoryRequest,
    user_id: str = Depends(get_user_id_from_token)
):
    importance = calculate_importance(request.text)
    embedding = generate_embedding(request.text, model_name="mxbai")

    memory_id = insert_memory(
        request.text,
        importance,
        user_id,
        embedding_model="mxbai"
    )
    insert_vector(memory_id, embedding, user_id, model_name="mxbai")

    return MemoryResponse(
        message="Memory stored successfully",
        memory_id=memory_id,
        importance=importance
    )


# ----------------------------------
# QUERY MEMORY
# ----------------------------------

@app.post("/query", response_model=QueryResponse)
def query_memory(
    request: QueryRequest,
    user_id: str = Depends(get_user_id_from_token)
):
    memories = retrieve_and_update(
        request.query,
        user_id,
        embedding_model="mxbai"
    )

    if not memories:
        return QueryResponse(
            top_memories=[],
            answer="I don't have enough information in my memories to answer this."
        )

    texts = [m["text"] for m in memories]

    answer = generate_answer(
        memories=texts,
        query=request.query,
        model=request.model if hasattr(request, "model") and request.model else "llama-3.3-70b-versatile"
    )

    return QueryResponse(
        top_memories=texts,
        answer=answer
    )


# ----------------------------------
# GET SINGLE MEMORY
# ----------------------------------

@app.get("/memory/{memory_id}")
def get_memory(
    memory_id: str,
    user_id: str = Depends(get_user_id_from_token)
):
    results = fetch_memories_by_ids([memory_id], user_id)

    if not results:
        raise HTTPException(status_code=404, detail="Memory not found")

    return results[0]


# ----------------------------------
# MANUAL DECAY TRIGGER
# ----------------------------------

@app.post("/memory/{memory_id}/decay")
def trigger_decay(
    memory_id: str,
    user_id: str = Depends(get_user_id_from_token)
):
    result = (
        supabase_client
        .table("memories")
        .select("*")
        .eq("id", memory_id)
        .eq("user_id", user_id)   # ✅ scoped to user — was missing
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Memory not found")

    memory = result.data[0]

    memory = apply_decay(memory)
    memory = update_memory_state(memory)

    update_memory_fields(
        memory_id,
        user_id,
        memory["strength"],
        memory["state"],
        now_utc().isoformat()
    )

    return {
        "memory_id": memory_id,
        "strength": memory["strength"],
        "state": memory["state"]
    }


# ----------------------------------
# HEALTH CHECK
# ----------------------------------

@app.get("/health")
def health():
    return {"status": "ok", "service": "Memora API"}