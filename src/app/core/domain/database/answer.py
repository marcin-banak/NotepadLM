from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any

@dataclass
class AnswerDB:
    id: Optional[int]
    user_id: int
    question: str
    answer_text: str
    title: str
    references: Dict[str, Dict[str, Any]]  # {"1": {"note_id": int, "chunk_id": int, "chunk_text": str}, ...}
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

