from typing import List
from app.core.domain.vectorstore.note import NoteVS
from abc import ABC, abstractmethod

class IVectorStore(ABC):
    @abstractmethod
    def upsert_full_notes(self, notes: List[NoteVS]):
        pass

    @abstractmethod
    def get_full_notes(self, user_id: int) -> List[NoteVS]:
        pass

    # --- VECTORSTORE 2: CHUNKI ---
    @abstractmethod
    def upsert_chunked_notes(self, notes: List[NoteVS]):
        pass

    @abstractmethod
    def get_chunked_notes(self, user_id: int) -> List[NoteVS]:
        pass

    @abstractmethod
    def retrieve_chunks(self, query: str, user_id: int, k: int = 4) -> List[NoteVS]:
        pass

    @abstractmethod
    def delete_note(self, note_id: int):
        pass