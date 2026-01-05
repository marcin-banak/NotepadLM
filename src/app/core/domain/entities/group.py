from dataclasses import dataclass, field
from typing import List, Optional

from app.core.domain.entities.note import NoteDB

@dataclass
class GroupDB:
    id: Optional[int]
    user_id: int
    summary: str = ""
    notes: List[NoteDB] = field(default_factory=list)

    def refresh_summary(self):
        if not self.notes:
            self.summary = "Brak notatek w grupie."
            return
            
        titles = [n.title for n in self.notes]
        self.summary = f"Grupa zawiera {len(self.notes)} notatek: " + ", ".join(titles)