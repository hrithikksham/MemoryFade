from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MemoryState:
    FRESH = "FRESH"
    ACTIVE = "ACTIVE"
    FADING = "FADING"
    ARCHIVED = "ARCHIVED"

class Memory(BaseModel):
    id: str
    text: str
    created_at: datetime
    importance: float
    strength: float
    last_accessed: datetime
    access_count: int
    state: str