from typing import List
from app.core.domain.vectorstore.note import NoteVS
from abc import ABC, abstractmethod

class IVectorStore(ABC):
    @abstractmethod
    def upsert_full_note(self, note: NoteVS):
        pass

    @abstractmethod
    def get_all_full_notes_with_embeddings(self) -> List[NoteVS]:
        pass

    # --- VECTORSTORE 2: CHUNKI ---
    @abstractmethod
    def upsert_chunked_note(self, note: NoteVS):
        pass

    @abstractmethod
    def delete_note_everywhere(self, note_id: int):
        pass