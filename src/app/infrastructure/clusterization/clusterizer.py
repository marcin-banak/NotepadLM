from typing import List
from umap import UMAP
from hdbscan import HDBSCAN
from bertopic import BERTopic
from bertopic.representation import KeyBERTInspired
from sklearn.feature_extraction.text import CountVectorizer

from app.core.domain.clusterization import NoteCluster, IClusterizer
from app.infrastructure.clusterization.clusterizer_config import ClusterizerConfig
from app.infrastructure.clusterization.llm_label_adapter import LLMLabelAdapter
from app.infrastructure.prompts.cluster_labeling_prompt import CLUSTER_NAMING_PROMPT


class Clusterizer(IClusterizer):
    def __init__(self, embedding_model, clusterizer_config: ClusterizerConfig):
        umap_model = UMAP(
            n_neighbors=clusterizer_config.umap_config.n_neighbors,
            n_components=clusterizer_config.umap_config.n_components,
            min_dist=clusterizer_config.umap_config.min_dist, 
            metric=clusterizer_config.umap_config.metric,
            random_state=42
        )

        hdbscan_model = HDBSCAN(
            min_cluster_size=clusterizer_config.hdbscan_config.min_cluster_size,
            metric=clusterizer_config.hdbscan_config.metric, 
            prediction_data=clusterizer_config.hdbscan_config.prediction_data
        )

        vectorizer_model = CountVectorizer(
            stop_words=clusterizer_config.vectorizer_config.stop_words,
            ngram_range=clusterizer_config.vectorizer_config.ngram_range,
            min_df=clusterizer_config.vectorizer_config.min_df,
            max_df=clusterizer_config.vectorizer_config.max_df
        )

        keybert_representation = KeyBERTInspired(
            top_n_words=clusterizer_config.bertopic_config.top_n_words
        )

        self.model = BERTopic(
            embedding_model=embedding_model,
            umap_model=umap_model,
            vectorizer_model=vectorizer_model,
            hdbscan_model=hdbscan_model,
            representation_model=keybert_representation,
            min_topic_size=clusterizer_config.bertopic_config.min_topic_size,
            calculate_probabilities=clusterizer_config.bertopic_config.calculate_probabilities,
            verbose=clusterizer_config.bertopic_config.verbose
        )

        self.llm_labeler = LLMLabelAdapter(
            llm_callable=clusterizer_config.bertopic_config.representation_model,
            prompt=CLUSTER_NAMING_PROMPT,
            max_docs=3
        ) if clusterizer_config.bertopic_config.representation_model else None

    def cluster_notes(self, notes: List[NoteCluster]) -> List[NoteCluster]:
        if not notes:
            return []

        texts = [note.content for note in notes]

        topics, _ = self.model.fit_transform(texts)

        info = self.model.get_topic_info()
        relevant_topics = info[info["Topic"] != -1]

        for note, topic_id in zip(notes, topics):
            note.cluster_id = int(topic_id)

        if self.llm_labeler:
            topic_labels = self.llm_labeler(
                topics=relevant_topics["Topic"].tolist(),
                documents=relevant_topics["Representative_Docs"].tolist(),
                keywords=relevant_topics["Representation"].tolist()
            )

            self.model.set_topic_labels(topic_labels)

        return notes

    def get_topic_info(self):
        return self.model.get_topic_info()

    def get_pretty_topic_labels(self):
        info = self.model.get_topic_info()
        
        if "CustomName" in info.columns:
            info['Name'] = info['CustomName'].map(lambda x: x[0] if isinstance(x, list) else x)
        
        return info

    def reduce_topics(self, notes: List[NoteCluster], nr_topics: int):
        texts = [note.content for note in notes]
        self.model.reduce_topics(texts, nr_topics=nr_topics)
        
        new_topics = self.model.topics_
        for note, topic_id in zip(notes, new_topics):
            note.cluster_id = int(topic_id)
        
        return notes