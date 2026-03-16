from pydantic import BaseModel

class MemoryRequest(BaseModel):
    text: str

class QueryRequest(BaseModel):
    query: str

class MemoryResponse(BaseModel):
    message: str
    memory_id: str

class QueryResponse(BaseModel):
    top_memories: list[str]
    answer: str