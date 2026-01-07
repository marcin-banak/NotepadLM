"""Note service for note-related operations."""

from typing import List, Optional
from app.core.domain.database import NoteDB
from app.core.domain.database import INoteRepository


class NoteService:
    """Service for note-related operations."""
    
    def __init__(self, repository: INoteRepository):
        self.repository = repository
    
    def create_note(self, title: str, content: str, user_id: int, group_id: Optional[int] = None) -> int:
        """Create a new note for a user."""
        note_db = NoteDB(
            id=None,
            title=title,
            content=content,
            user_id=user_id,
            group_id=group_id
        )
        return self.repository.create_note(note_db)
    
    def get_note(self, note_id: int, user_id: int) -> Optional[NoteDB]:
        """Get a note by ID, ensuring it belongs to the user."""
        note = self.repository.get_note(note_id)
        if note and note.user_id == user_id:
            return note
        return None
    
    def get_notes_by_user(self, user_id: int) -> List[NoteDB]:
        """Get all notes for a user."""
        # We need to add this method to repository or filter here
        # For now, we'll need to add get_notes_by_user to repository
        return self.repository.get_notes_by_user(user_id)
    
    def update_note(self, note_id: int, user_id: int, title: Optional[str] = None, 
                    content: Optional[str] = None, group_id: Optional[int] = None) -> Optional[int]:
        """Update a note, ensuring it belongs to the user."""
        note = self.repository.get_note(note_id)
        if not note or note.user_id != user_id:
            return None
        
        # Update fields
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        if group_id is not None:
            note.group_id = group_id
        
        return self.repository.update_note(note)
    
    def delete_note(self, note_id: int, user_id: int) -> bool:
        """Delete a note, ensuring it belongs to the user."""
        note = self.repository.get_note(note_id)
        if not note or note.user_id != user_id:
            return False
        return self.repository.delete_note(note_id)

