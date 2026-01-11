from typing import List
import langchain  # Ensure langchain is imported before bertopic checks for it
import langchain_community
import langchain_core
from umap import UMAP
from hdbscan import HDBSCAN
from bertopic import BERTopic
from bertopic.representation import LangChain

from app.core.domain.clusterization import NoteCluster, IClusterizer
from app.infrastructure.clusterization.clusterizer_config import ClusterizerConfig

CLUSTER_NAMING_PROMPT = """
Jesteś ekspertem od kategoryzacji treści. Na podstawie poniższych słów kluczowych 
oraz fragmentów notatek, wymyśl krótką, profesjonalną nazwę dla tej grupy tematów.
Zwróć TYLKO nazwę (maksymalnie 3-4 słowa).

Słowa kluczowe: [KEYWORDS]
Przykładowe notatki: [DOCUMENTS]
Nazwa grupy:"""

class Clusterizer(IClusterizer):
    def __init__(self, embedding_model, clusterizer_config: ClusterizerConfig):
        umap_model = UMAP(
            n_neighbors=clusterizer_config.umap_config.n_neighbors,
            n_components=clusterizer_config.umap_config.n_components,
            min_dist=clusterizer_config.umap_config.min_dist, 
            metric=clusterizer_config.umap_config.metric
        )

        hdbscan_model = HDBSCAN(
            min_cluster_size=clusterizer_config.hdbscan_config.min_cluster_size,
            metric=clusterizer_config.hdbscan_config.metric, 
            prediction_data=clusterizer_config.hdbscan_config.prediction_data
        )

        self.model = BERTopic(
            embedding_model=embedding_model,
            umap_model=umap_model,
            hdbscan_model=hdbscan_model,
            min_topic_size=clusterizer_config.bertopic_config.min_topic_size,
            # representation_model=LangChain(clusterizer_config.bertopic_config.representation_model, prompt=CLUSTER_NAMING_PROMPT),
            calculate_probabilities=clusterizer_config.bertopic_config.calculate_probabilities,
            verbose=clusterizer_config.bertopic_config.verbose
        )

    def cluster_notes(self, notes: List[NoteCluster]) -> List[NoteCluster]:
        if not notes:
            return []

        texts = [note.content for note in notes]

        topics, _ = self.model.fit_transform(texts)

        for note, topic_id in zip(notes, topics):
            note.cluster_id = int(topic_id)

        return notes

    def get_topic_info(self):
        return self.model.get_topic_info()

    def get_pretty_topic_labels(self):
        info = self.model.get_topic_info()
        
        if "LangChain" in info.columns:
            return {
                int(row.Topic): row.LangChain[0].strip() 
                for row in info.itertuples() if row.Topic != -1
            }
        return {}

    def reduce_topics(self, notes: List[NoteCluster], nr_topics: int):
        texts = [note.content for note in notes]
        self.model.reduce_topics(texts, nr_topics=nr_topics)
        
        new_topics = self.model.topics_
        for note, topic_id in zip(notes, new_topics):
            note.cluster_id = int(topic_id)
        
        return notes