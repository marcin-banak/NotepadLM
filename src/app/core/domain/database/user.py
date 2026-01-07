from dataclasses import dataclass
from typing import Optional

@dataclass
class UserDB:
    id: Optional[int]
    name: str
    password_hash: str