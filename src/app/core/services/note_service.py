"""Note service for note-related operations."""

from typing import List, Optional, Tuple
from app.core.domain.database import NoteDB, GroupDB
from app.core.domain.database import INoteRepository
from app.core.domain.vectorstore import IVectorStore, NoteVS
from app.core.domain.clusterization import IClusterizer, NoteCluster


class NoteService:
    """Service for note-related operations."""
    
    def __init__(
        self, 
        repository: INoteRepository,
        vector_store: IVectorStore,
        clusterizer: IClusterizer
    ):
        self.repository = repository
        self.vector_store = vector_store
        self.clusterizer = clusterizer
    
    def _note_db_to_note_vs(self, note_db: NoteDB) -> NoteVS:
        """Convert NoteDB to NoteVS for vectorstore operations."""
        # Combine title and content for better vectorization
        full_content = f"{note_db.title}\n{note_db.content}" if note_db.title else note_db.content
        return NoteVS(
            id=note_db.id,
            user_id=note_db.user_id,
            chunk_id=None,
            content=full_content,
            embedding=None
        )
    
    def _note_db_to_note_cluster(self, note_db: NoteDB) -> NoteCluster:
        """Convert NoteDB to NoteCluster for clustering operations."""
        # Combine title and content for better clustering
        full_content = f"{note_db.title}\n{note_db.content}" if note_db.title else note_db.content
        return NoteCluster(
            id=note_db.id,
            user_id=note_db.user_id,
            cluster_id=None,
            content=full_content
        )
    
    def _sync_to_vectorstore(self, note: NoteDB):
        """Sync a note to the vectorstore (both full and chunked)."""
        import json
        import os
        LOG_PATH = "/Users/marbook/projects/NotepadLM/.cursor/debug.log"
        def _log(hypothesis_id, location, message, data=None):
            try:
                log_entry = {
                    "sessionId": "debug-session",
                    "runId": "run1",
                    "hypothesisId": hypothesis_id,
                    "location": location,
                    "message": message,
                    "data": data or {},
                    "timestamp": int(__import__("time").time() * 1000)
                }
                with open(LOG_PATH, "a") as f:
                    f.write(json.dumps(log_entry) + "\n")
            except:
                pass
        
        # #region agent log
        _log("A", "note_service.py:_sync_to_vectorstore", "Entry", {"note_id": note.id, "note_id_type": type(note.id).__name__, "user_id": note.user_id})
        # #endregion
        note_vs = self._note_db_to_note_vs(note)
        # #region agent log
        _log("A", "note_service.py:_sync_to_vectorstore", "Converted to NoteVS", {"note_id": note.id, "note_vs_id": note_vs.id, "note_vs_id_type": type(note_vs.id).__name__})
        # #endregion
        try:
            self.vector_store.upsert_full_notes([note_vs])
            # #region agent log
            _log("B", "note_service.py:_sync_to_vectorstore", "upsert_full_notes succeeded", {"note_id": note.id})
            # #endregion
        except Exception as e:
            # #region agent log
            _log("B", "note_service.py:_sync_to_vectorstore", "upsert_full_notes failed (non-blocking)", {"note_id": note.id, "error": str(e), "error_type": type(e).__name__})
            # #endregion
            # Don't raise - allow note creation to succeed even if vectorstore fails
            import logging
            logging.getLogger(__name__).warning(f"Failed to sync note {note.id} to vectorstore: {e}")
        try:
            self.vector_store.upsert_chunked_notes([note_vs])
            # #region agent log
            _log("B", "note_service.py:_sync_to_vectorstore", "upsert_chunked_notes succeeded", {"note_id": note.id})
            # #endregion
        except Exception as e:
            # #region agent log
            _log("B", "note_service.py:_sync_to_vectorstore", "upsert_chunked_notes failed (non-blocking)", {"note_id": note.id, "error": str(e), "error_type": type(e).__name__})
            # #endregion
            # Don't raise - allow note creation to succeed even if vectorstore fails
            import logging
            logging.getLogger(__name__).warning(f"Failed to sync note {note.id} chunks to vectorstore: {e}")
    
    def _recalculate_groups(self, user_id: int):
        """Recalculate groups for a user by clustering their notes."""
        import logging
        try:
            # Get all notes for the user
            notes = self.repository.get_notes_by_user(user_id)
            
            # Skip clustering if no notes
            if not notes:
                return
            
            # Delete all existing groups for the user
            self.repository.delete_groups_by_user(user_id)
            
            # Convert notes to NoteCluster format
            note_clusters = [self._note_db_to_note_cluster(note) for note in notes]
            
            # Cluster the notes
            clustered_notes = self.clusterizer.cluster_notes(note_clusters)
            
            # Get topic info from clusterizer
            topic_info = self.clusterizer.get_pretty_topic_labels()
            
            # Create a mapping of cluster_id to topic name
            # topic_info is a pandas DataFrame with columns: Topic, Count, Name, etc.
            cluster_to_topic_name = {}
            if topic_info is not None and not topic_info.empty:
                for _, row in topic_info.iterrows():
                    cluster_id = int(row['Topic'])
                    topic_name = str(row['Name']) if 'Name' in row else f"Topic {cluster_id}"
                    cluster_to_topic_name[cluster_id] = topic_name
            
            # Group notes by cluster_id (excluding outliers with cluster_id=-1)
            cluster_to_notes = {}
            for note_cluster in clustered_notes:
                cluster_id = note_cluster.cluster_id
                if cluster_id is not None and cluster_id != -1:
                    if cluster_id not in cluster_to_notes:
                        cluster_to_notes[cluster_id] = []
                    cluster_to_notes[cluster_id].append(note_cluster)
            
            # Create groups for each cluster and assign notes
            for cluster_id, cluster_notes in cluster_to_notes.items():
                # Get topic name for this cluster, or use default
                topic_name = cluster_to_topic_name.get(cluster_id, f"Topic {cluster_id}")
                
                # Create group
                group = GroupDB(
                    id=None,
                    user_id=user_id,
                    summary=topic_name,
                    notes=[]
                )
                group_id = self.repository.create_group(group)
                
                # Assign notes to this group
                for note_cluster in cluster_notes:
                    self.repository.update_note_group_id(note_cluster.id, group_id)
        except Exception as e:
            # Don't raise - allow note operation to succeed even if clustering fails
            logging.getLogger(__name__).error(f"Failed to recalculate groups for user {user_id}: {e}", exc_info=True)
    
    def create_note(self, title: str, content: str, user_id: int, group_id: Optional[int] = None) -> int:
        """Create a new note for a user."""
        note_db = NoteDB(
            id=None,
            title=title,
            content=content,
            user_id=user_id,
            group_id=group_id
        )
        note_id = self.repository.create_note(note_db)
        
        # Get the created note to sync to vectorstore
        note = self.repository.get_note(note_id)
        if note:
            # Sync to vectorstore
            self._sync_to_vectorstore(note)
            # Recalculate groups
            self._recalculate_groups(user_id)
        
        return note_id
    
    def bulk_create_notes(self, notes_data: List[dict], user_id: int) -> Tuple[List[int], List[dict]]:
        """Create multiple notes for a user efficiently.
        
        Args:
            notes_data: List of dicts with 'title', 'content', and optionally 'group_id'
            user_id: The user ID to create notes for
            
        Returns:
            Tuple of (created_note_ids, failed_notes) where failed_notes contains
            dicts with 'index', 'title', and 'error' keys
        """
        created_ids = []
        failed_notes = []
        created_note_objects = []
        
        # Create all notes in the database first
        for i, note_data in enumerate(notes_data):
            try:
                title = note_data.get("title", "Untitled Note")
                content = note_data.get("content", "")
                group_id = note_data.get("group_id")
                
                note_db = NoteDB(
                    id=None,
                    title=title,
                    content=content,
                    user_id=user_id,
                    group_id=group_id
                )
                note_id = self.repository.create_note(note_db)
                created_ids.append(note_id)
                
                # Get the created note for vectorstore sync
                note = self.repository.get_note(note_id)
                if note:
                    created_note_objects.append(note)
            except Exception as e:
                failed_notes.append({
                    "index": i,
                    "title": note_data.get("title", "Untitled Note"),
                    "error": str(e)
                })
        
        # Sync all created notes to vectorstore in batches
        if created_note_objects:
            note_vs_list = [self._note_db_to_note_vs(note) for note in created_note_objects]
            
            # Sync full notes
            try:
                self.vector_store.upsert_full_notes(note_vs_list)
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Failed to sync full notes to vectorstore: {e}")
            
            # Sync chunked notes
            try:
                self.vector_store.upsert_chunked_notes(note_vs_list)
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Failed to sync chunked notes to vectorstore: {e}")
            
            # Recalculate groups once at the end
            self._recalculate_groups(user_id)
        
        return created_ids, failed_notes
    
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
        
        # Store old note for vectorstore deletion
        old_note = note
        
        # Update fields
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        if group_id is not None:
            note.group_id = group_id
        
        updated_id = self.repository.update_note(note)
        
        if updated_id:
            # Get updated note
            updated_note = self.repository.get_note(updated_id)
            if updated_note:
                # Delete old note from vectorstore and add updated one
                self.vector_store.delete_note(old_note.id)
                self._sync_to_vectorstore(updated_note)
                # Recalculate groups
                self._recalculate_groups(user_id)
        
        return updated_id
    
    def delete_note(self, note_id: int, user_id: int) -> bool:
        """Delete a note, ensuring it belongs to the user."""
        import json
        import os
        LOG_PATH = "/Users/marbook/projects/NotepadLM/.cursor/debug.log"
        def _log(hypothesis_id, location, message, data=None):
            try:
                log_entry = {
                    "sessionId": "debug-session",
                    "runId": "run1",
                    "hypothesisId": hypothesis_id,
                    "location": location,
                    "message": message,
                    "data": data or {},
                    "timestamp": int(__import__("time").time() * 1000)
                }
                with open(LOG_PATH, "a") as f:
                    f.write(json.dumps(log_entry) + "\n")
            except:
                pass
        
        # #region agent log
        _log("E", "note_service.py:delete_note", "Entry", {"note_id": note_id, "user_id": user_id})
        # #endregion
        note = self.repository.get_note(note_id)
        if not note or note.user_id != user_id:
            # #region agent log
            _log("E", "note_service.py:delete_note", "Note not found or access denied", {"note_id": note_id, "user_id": user_id, "note_exists": note is not None, "note_user_id": note.user_id if note else None})
            # #endregion
            return False
        
        # Delete from vectorstore first (non-blocking)
        try:
            # #region agent log
            _log("E", "note_service.py:delete_note", "Calling vectorstore.delete_note", {"note_id": note_id})
            # #endregion
            self.vector_store.delete_note(note_id)
            # #region agent log
            _log("E", "note_service.py:delete_note", "vectorstore.delete_note succeeded", {"note_id": note_id})
            # #endregion
        except Exception as e:
            # #region agent log
            _log("E", "note_service.py:delete_note", "vectorstore.delete_note failed (non-blocking)", {"note_id": note_id, "error": str(e), "error_type": type(e).__name__})
            # #endregion
            # Don't raise - allow database deletion to proceed even if vectorstore fails
            import logging
            logging.getLogger(__name__).warning(f"Failed to delete note {note_id} from vectorstore: {e}")
        
        # Delete from database
        success = self.repository.delete_note(note_id)
        # #region agent log
        _log("E", "note_service.py:delete_note", "Database delete result", {"note_id": note_id, "success": success})
        # #endregion
        
        if success:
            # Recalculate groups
            self._recalculate_groups(user_id)
        
        return success
    
    def query_relevant_notes(
        self, 
        query: str, 
        user_id: int, 
        k: int = 10, 
        threshold: float = 0.4
    ) -> List[dict]:
        """Query for relevant notes with chunk markers.
        
        Args:
            query: The search query string
            user_id: The user ID to search notes for
            k: Maximum number of chunks to retrieve
            threshold: Minimum similarity score threshold
            
        Returns:
            List of dicts with keys:
                - note: NoteDB object
                - chunk_text: The relevant chunk text
                - chunk_start: Start position of chunk in note content
                - chunk_end: End position of chunk in note content
                - relevance_score: Similarity score for the chunk
        """
        # Retrieve relevant chunks from vectorstore
        relevant_chunks_with_scores = self.vector_store.retrieve_chunks(query, user_id, k=k, threshold=threshold)
        
        results = []
        seen_note_ids = set()
        
        for chunk_vs, relevance_score in relevant_chunks_with_scores:
            # Skip if we've already processed this note
            if chunk_vs.id in seen_note_ids:
                continue
            
            # Get the full note from repository
            note = self.repository.get_note(chunk_vs.id)
            if not note or note.user_id != user_id:
                continue
            
            # Find the chunk position in the note content
            # Note: chunks are created from full_content = title + "\n" + content
            # But we need to find the position in just the content field
            chunk_text = chunk_vs.content
            note_content = note.content or ""
            note_title = note.title or ""
            
            # Reconstruct the full content as it was when chunked
            full_content_for_chunking = f"{note_title}\n{note_content}" if note_title else note_content
            
            # Try to find the chunk in the full content (title + content)
            chunk_start_in_full = full_content_for_chunking.find(chunk_text)
            
            # Calculate the offset: title length + newline if title exists
            title_offset = len(note_title) + 1 if note_title else 0
            
            if chunk_start_in_full != -1:
                # Chunk found in full content
                if chunk_start_in_full >= title_offset:
                    # Chunk is in the content part (not in title)
                    chunk_start = chunk_start_in_full - title_offset
                    chunk_end = chunk_start + len(chunk_text)
                else:
                    # Chunk starts in title, find where it overlaps into content
                    # Find the part of chunk that's in content
                    overlap_start = max(0, title_offset - chunk_start_in_full)
                    chunk_start = 0
                    chunk_end = len(chunk_text) - overlap_start
            else:
                # Try to find a substring match in content only
                # Remove title prefix from chunk if it starts with title
                chunk_in_content = chunk_text
                if note_title and chunk_text.startswith(note_title):
                    # Remove title and newline from start of chunk
                    title_prefix = f"{note_title}\n"
                    if chunk_text.startswith(title_prefix):
                        chunk_in_content = chunk_text[len(title_prefix):]
                
                # Try to find the content part in note content
                chunk_start = note_content.find(chunk_in_content)
                chunk_end = chunk_start + len(chunk_in_content) if chunk_start != -1 else -1
                
                # If still not found, try fuzzy matching
                if chunk_start == -1:
                    min_match_length = max(50, int(len(chunk_in_content) * 0.7))
                    for i in range(len(note_content) - min_match_length + 1):
                        substring = note_content[i:i + len(chunk_in_content)]
                        if len(substring) >= min_match_length:
                            # Simple similarity check
                            matches = sum(c1 == c2 for c1, c2 in zip(chunk_in_content[:len(substring)], substring))
                            if matches / len(substring) > 0.7:
                                chunk_start = i
                                chunk_end = min(i + len(chunk_in_content), len(note_content))
                                break
                
                # If still not found, estimate position based on chunk_id
                if chunk_start == -1 and chunk_vs.chunk_id is not None:
                    chunk_size = 1000
                    chunk_overlap = 180
                    # Estimate: each chunk after the first starts at (chunk_id * (chunk_size - chunk_overlap))
                    # Account for title offset
                    estimated_start_in_full = chunk_vs.chunk_id * (chunk_size - chunk_overlap)
                    if estimated_start_in_full >= title_offset:
                        estimated_start = estimated_start_in_full - title_offset
                        chunk_start = min(estimated_start, len(note_content))
                        chunk_end = min(chunk_start + len(chunk_in_content), len(note_content))
                    else:
                        chunk_start = 0
                        chunk_end = min(len(chunk_in_content), len(note_content))
            
            results.append({
                "note": note,
                "chunk_text": chunk_text,
                "chunk_start": chunk_start if chunk_start != -1 else 0,
                "chunk_end": chunk_end if chunk_end != -1 else len(note_content),
                "relevance_score": relevance_score
            })
            
            seen_note_ids.add(chunk_vs.id)
        
        return results

