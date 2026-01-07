from dataclasses import dataclass, field
from typing import List, Optional

from app.core.domain.database.note import NoteDB

@dataclass
class GroupDB:
    id: Optional[int]
    user_id: int
    summary: str = ""
    notes: List[int] = field(default_factory=list)