from dataclasses import dataclass
from typing import Optional, List

@dataclass
class NoteVS:
    id: int
    user_id: int
    chunk_id: Optional[int]
    content: str
    embedding: Optional[List[float]]