from typing import List, Tuple
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
    def retrieve_chunks(self, query: str, user_id: int, k: int = 4, threshold: float = 0.4) -> List[Tuple[NoteVS, float]]:
        """Retrieve relevant chunks with relevance scores.
        
        Returns:
            List of tuples (NoteVS, relevance_score) sorted by relevance descending.
        """
        pass

    @abstractmethod
    def delete_note(self, note_id: int):
        pass