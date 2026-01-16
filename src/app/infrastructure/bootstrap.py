import os
# Monkey-patch for bertopic compatibility with newer langchain versions
# bertopic tries to import from langchain.docstore.document which doesn't exist in langchain >= 1.0
import sys
import types
from langchain_core.documents import Document

# Create a fake langchain.docstore module
if 'langchain.docstore' not in sys.modules:
    docstore_module = types.ModuleType('langchain.docstore')
    docstore_module.document = types.ModuleType('langchain.docstore.document')
    docstore_module.document.Document = Document
    sys.modules['langchain.docstore'] = docstore_module
    sys.modules['langchain.docstore.document'] = docstore_module.document

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI

from app.infrastructure.database.models import Base, Answer
from app.infrastructure.database.repository import AppRepository

data_storage_path = "./data_storage"
os.makedirs(data_storage_path, exist_ok=True)

engine = create_engine(
    f"sqlite:///{data_storage_path}/notepadlm.db",
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

database_repository = AppRepository(SessionLocal)


embeddings = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", api_key=os.getenv("GOOGLE_API_KEY"))

from app.infrastructure.vectorstore.vectorstore import VectorStore

vector_store = VectorStore(embeddings, f"{data_storage_path}/vector_storage")

from app.infrastructure.clusterization.clusterizer import Clusterizer
from app.infrastructure.clusterization.clusterizer_config import (
    UMAPConfig, HDBSCANConfig, BERTopicConfig, VectorizerConfig, ClusterizerConfig
)

def llm_callable(prompt: str) -> str:
    response = llm.invoke(prompt)
    return response.content.strip() if response and getattr(response, "content", None) else "Unnamed Topic"

umap_config = UMAPConfig(
    n_neighbors=10,
    n_components=5,
    min_dist=0.0,
    metric='cosine'
)
hdbscan_config = HDBSCANConfig(
    min_cluster_size=8,
    metric='euclidean',
    prediction_data=True
)
vectorizer_config = VectorizerConfig(
    stop_words='english',
    ngram_range=(1, 2),
    min_df=2,
    max_df=0.90
)
bertopic_config = BERTopicConfig(
    min_topic_size=8,
    top_n_words=40,
    representation_model=llm_callable,
    calculate_probabilities=False,
    verbose=True
)
clusterizer_config = ClusterizerConfig(
    umap_config=umap_config,
    hdbscan_config=hdbscan_config,
    vectorizer_config=vectorizer_config,
    bertopic_config=bertopic_config
)

clusterizer = Clusterizer(embeddings, clusterizer_config)