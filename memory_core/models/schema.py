from pydantic import BaseModel
from typing import Optional

class ModelConfig(BaseModel):
    embedding: str = "mxbai-embed-large"
    llm: str = "llama3-70b-8192"

class MemoryRequest(BaseModel):
    text: str
    llm_config: Optional[ModelConfig] = None  # renamed

class QueryRequest(BaseModel):
    query: str
    llm_config: Optional[ModelConfig] = None  # renamed

class MemoryResponse(BaseModel):
    message: str
    memory_id: str
    importance: float

class QueryResponse(BaseModel):
    top_memories: list[str]
    answer: str
    models_used: Optional[ModelConfig] = None
    latency_ms: Optional[int] = None