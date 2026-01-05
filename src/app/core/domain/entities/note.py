from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class NoteDB:
    id: Optional[int]
    title: str
    content: str
    user_id: int
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    group_id: Optional[int] = None

    def update_content(self, new_content: str):
        self.content = new_content
        self.updated_at = datetime.now()