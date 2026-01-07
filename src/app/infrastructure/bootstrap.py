from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from langchain_huggingface import HuggingFaceEmbeddings

from app.infrastructure.database.models import Base
from app.infrastructure.database.repository import AppRepository

engine = create_engine(
    "sqlite:///notepadlm.db",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

database_repository = AppRepository(SessionLocal)


# from app.infrastructure.vectorstore.vectorstore import VectorStore

# embeddings = "" # HuggingFaceEmbeddings(model_name="Multilingual-e5-large")
# vector_store = VectorStore(embeddings)

# from app.infrastructure.clusterization.clusterizer import NoteClusteringService

# clusterizer = NoteClusteringService(embeddings)