from pydantic import BaseModel

class MemoryRequest(BaseModel):
    text: str

class QueryRequest(BaseModel):
    query: str

class MemoryResponse(BaseModel):
    message: str
    memory_id: str
    importance: float

class QueryResponse(BaseModel):
    answer: str