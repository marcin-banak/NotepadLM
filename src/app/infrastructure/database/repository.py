from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional, Type, Any, Callable

from app.core.domain.entities import UserDB, NoteDB, GroupDB
from app.core.domain.repositories import INoteRepository
from app.infrastructure.database.models import User, Group, Note

class AppRepository(INoteRepository):
    def __init__(self, session_factory: Callable[[], Session]):
        self.session_factory = session_factory

    def _get_session(self) -> Session:
        return self.session_factory()

    # --- USER OPERATIONS ---
    def create_user(self, user_db: UserDB) -> int:
        with self._get_session() as session:
            with session.begin():
                user = User(name=user_db.name, password=user_db.password_hash)
                session.add(user)
                session.flush()
                return user.id  # Tu expunge jest zbędne, bo zwracamy int

    def get_user(self, user_id: int) -> Optional[UserDB]:
        with self._get_session() as session:
            user = session.get(User, user_id)
            if user:
                return UserDB(id=user.id, name=user.name, password_hash=user.password)
            return None

    # --- GROUP OPERATIONS ---
    def create_group(self, group_db: GroupDB) -> int:
        with self._get_session() as session:
            with session.begin():
                group = Group(user_id=group_db.user_id, summary=group_db.summary)
                session.add(group)
                session.flush()
                return group.id

    def get_group(self, group_id: int) -> Optional[GroupDB]:
        with self._get_session() as session:
            # Używamy selectinload, aby pobrać notatki od razu w jednej sesji
            group = session.get(Group, group_id)
            if group:
                # Mapowanie robimy WEWNĄTRZ sesji
                notes_domain = [
                    NoteDB(id=n.id, title=n.title, content=n.content, 
                           user_id=n.user_id, group_id=n.group_id) 
                    for n in group.notes
                ]
                return GroupDB(id=group.id, user_id=group.user_id, 
                               summary=group.summary, notes=notes_domain)
            return None

    def get_groups_by_user(self, user_id: int) -> List[GroupDB]:
        with self._get_session() as session:
            stmt = select(Group).where(Group.user_id == user_id)
            groups = session.scalars(stmt).all()
            
            results = []
            for g in groups:
                # Najpierw wyciągamy notatki, póki sesja trwa
                notes = [NoteDB(id=n.id, title=n.title, content=n.content, 
                                user_id=n.user_id, group_id=n.group_id) 
                         for n in g.notes]
                results.append(GroupDB(id=g.id, user_id=g.user_id, 
                                       summary=g.summary, notes=notes))
            return results

    # --- NOTE OPERATIONS ---
    def create_note(self, note_db: NoteDB) -> int:
        with self._get_session() as session:
            with session.begin():
                note = Note(title=note_db.title, content=note_db.content, 
                            user_id=note_db.user_id, group_id=note_db.group_id)
                session.add(note)
                session.flush()
                return note.id

    def update_note(self, note_db: NoteDB) -> Optional[int]:
        # Poprawione przekazywanie ID do generycznej metody
        return self._update_entity(Note, note_db.id, 
                                   title=note_db.title, 
                                   content=note_db.content, 
                                   group_id=note_db.group_id)

    # --- GENERIC OPERATIONS ---
    def _update_entity(self, entity_class: Type, entity_id: int, **kwargs) -> Optional[int]:
        with self._get_session() as session:
            with session.begin():
                entity = session.get(entity_class, entity_id)
                if entity:
                    for key, value in kwargs.items():
                        # Pomijamy wartości None, chyba że chcesz czyścić pole w bazie
                        if value is not None and hasattr(entity, key):
                            setattr(entity, key, value)
                    session.flush()
                    return entity.id # Zwracamy ID (int)
                return None

    def delete_entity(self, entity_class: Type, entity_id: int) -> bool:
        with self._get_session() as session:
            with session.begin():
                entity = session.get(entity_class, entity_id)
                if entity:
                    session.delete(entity)
                    return True
                return False