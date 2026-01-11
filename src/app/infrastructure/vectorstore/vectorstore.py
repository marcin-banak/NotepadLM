from typing import List
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.core.domain.vectorstore import NoteVS, IVectorStore

class VectorStore(IVectorStore):
    def __init__(self, embeddings: HuggingFaceEmbeddings, db_path: str = "./vector_storage"):
        self.db_path = db_path
        self.embeddings = embeddings
        self.full_notes_dir = f"{db_path}/full_notes"
        self.chunked_notes_dir = f"{db_path}/chunks"
        
        # Konfiguracja splittera dla drugiego vectorstore
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=180
        )

    def _get_store(self, path: str, collection: str) -> Chroma:
        try:
            store = Chroma(
                persist_directory=path,
                embedding_function=self.embeddings,
                collection_name=collection
            )
            return store
        except Exception as e:
            raise

    # --- VECTORSTORE 1: PEŁNE NOTATKI ---
    def upsert_full_notes(self, notes: List[NoteVS]):
        try:
            store = self._get_store(self.full_notes_dir, "full_notes")
            docs = []
            ids = []
            for note in notes:
                doc = Document(
                    page_content=note.content or "",
                    metadata={"user_id": note.user_id}
                )
                docs.append(doc)
                note_id_str = str(note.id) if note.id is not None else None
                ids.append(note_id_str)
            store.add_documents(documents=docs, ids=ids)
        except Exception as e:
            raise

    def get_full_notes(self, user_id: int) -> List[NoteVS]:
        store = self._get_store(self.full_notes_dir, "full_notes")
        
        data = store.get(where={"user_id": user_id}, include=["embeddings", "documents", "metadatas"])

        results = []
        
        ids = data.get("ids", [])
        embeddings = data.get("embeddings", [])
        documents = data.get("documents", [])
        metadatas = data.get("metadatas", [])

        for i in range(len(ids)):
            results.append(NoteVS(
                id=int(ids[i]),
                user_id=int(metadatas[i]["user_id"]),
                chunk_id=None,
                content=documents[i],
                embedding=embeddings[i]
            ))
        return results

    # --- VECTORSTORE 2: CHUNKI ---
    def upsert_chunked_notes(self, notes: List[NoteVS]):
        try:
            store = self._get_store(self.chunked_notes_dir, "note_chunks")
            
            docs = []
            chunk_ids = []
            for note in notes:
                try:
                    store.delete(where={"parent_note_id": note.id})
                except Exception as e:
                    raise
            
            for note in notes:
                chunks = self.splitter.split_text(note.content or "")
                for i, chunk_text in enumerate(chunks):
                    docs.append(Document(
                        page_content=chunk_text,
                        metadata={
                            "parent_note_id": note.id,
                            "chunk_id": i,
                            "user_id": note.user_id
                        }
                    ))
                    chunk_ids.append(f"{note.id}_chunk_{i}")

            if docs:
                store.add_documents(documents=docs, ids=chunk_ids)
        except Exception as e:
            raise

    def get_chunked_notes(self, user_id: int) -> List[NoteVS]:
        store = self._get_store(self.chunked_notes_dir, "note_chunks")
        data = store.get(where={"user_id": user_id}, include=["embeddings", "documents", "metadatas"])

        results = []
        ids = data.get("ids", [])
        embeddings = data.get("embeddings", [])
        documents = data.get("documents", [])
        metadatas = data.get("metadatas", [])

        for i in range(len(ids)):
            results.append(NoteVS(
                id=int(metadatas[i]["parent_note_id"]),
                user_id=int(metadatas[i]["user_id"]),
                chunk_id=int(metadatas[i]["chunk_id"]),
                content=documents[i],
                embedding=embeddings[i] if embeddings else None
            ))
        return results

    def retrieve_chunks(self, query: str, user_id: int, k: int = 4) -> List[NoteVS]:
        store = self._get_store(self.chunked_notes_dir, "note_chunks")
        
        # E5 wymaga prefiksu 'query: ' dla zapytania
        relevant_chunks = store.similarity_search(
            query=f"query: {query}",
            k=k,
            filter={"user_id": user_id}
        )
        
        return [NoteVS(
            id=int(chunk.metadata["parent_note_id"]),
            chunk_id=int(chunk.metadata["chunk_id"]),
            user_id=int(chunk.metadata["user_id"]),
            content=chunk.page_content,
            embedding=None
        ) for chunk in relevant_chunks]

    def delete_note(self, note_id: int):
        try:
            full_store = self._get_store(self.full_notes_dir, "full_notes")
            try:
                full_store.delete(ids=[str(note_id)])
            except Exception as e:
                raise
            
            chunk_store = self._get_store(self.chunked_notes_dir, "note_chunks")
            try:
                chunk_store.delete(where={"parent_note_id": note_id})
            except Exception as e:
                raise
        except Exception as e:
            raise