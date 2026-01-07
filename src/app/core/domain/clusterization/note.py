from dataclasses import dataclass
from typing import Optional

@dataclass
class NoteCluster:
    id: int
    user_id: int
    cluster_id: Optional[int]
    content: str