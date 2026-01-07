from abc import ABC, abstractmethod
from typing import List, Optional
from app.core.domain.database import UserDB, NoteDB, GroupDB

class INoteRepository(ABC):
    # --- USER OPERATIONS ---
    @abstractmethod
    def create_user(self, user_db: UserDB) -> int:
        """Tworzy nowego użytkownika i zwraca jego ID."""
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[UserDB]:
        """Pobiera użytkownika po ID."""
        pass

    @abstractmethod
    def get_user_by_name(self, username: str) -> Optional[UserDB]:
        """Pobiera użytkownika po nazwie."""
        pass

    @abstractmethod
    def update_user(self, user_db: UserDB) -> Optional[int]:
        """Aktualizuje dane użytkownika."""
        pass

    # --- GROUP OPERATIONS ---
    @abstractmethod
    def create_group(self, group_db: GroupDB) -> int:
        """Tworzy nową grupę i zwraca jej ID."""
        pass

    @abstractmethod
    def get_group(self, group_id: int) -> Optional[GroupDB]:
        """Pobiera grupę wraz z jej notatkami."""
        pass

    @abstractmethod
    def get_groups_by_user(self, user_id: int) -> List[GroupDB]:
        """Pobiera wszystkie grupy należące do użytkownika."""
        pass

    @abstractmethod
    def update_group(self, group_db: GroupDB) -> Optional[int]:
        """Aktualizuje metadane grupy."""
        pass

    # --- NOTE OPERATIONS ---
    @abstractmethod
    def create_note(self, note_db: NoteDB) -> int:
        """Tworzy nową notatkę i zwraca jej ID."""
        pass

    @abstractmethod
    def get_note(self, note_id: int) -> Optional[NoteDB]:
        """Pobiera pojedynczą notatkę."""
        pass

    @abstractmethod
    def get_notes_by_user(self, user_id: int) -> List[NoteDB]:
        """Pobiera wszystkie notatki użytkownika."""
        pass

    @abstractmethod
    def update_note(self, note_db: NoteDB) -> Optional[int]:
        """Aktualizuje treść lub przypisanie notatki."""
        pass

    # --- DELETION ---
    @abstractmethod
    def delete_user(self, user_id: int) -> bool: pass
    
    @abstractmethod
    def delete_group(self, group_id: int) -> bool: pass
    
    @abstractmethod
    def delete_note(self, note_id: int) -> bool: pass