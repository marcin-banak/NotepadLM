from typing import List
from bertopic import BERTopic

from app.core.domain.clusterization import NoteCluster, IClusterizer


class NoteClusteringService(IClusterizer):
    def __init__(self, embedding_model, min_topic_size: int = 5):
        """
        :param embedding_model: Obiekt modelu embeddingowego (np. SentenceTransformer)
        :param min_topic_size: Minimalna liczba notatek, by utworzyć temat
        """
        # Inicjalizacja BERTopic z przekazanym modelem
        self.model = BERTopic(
            embedding_model=embedding_model,
            min_topic_size=min_topic_size,
            calculate_probabilities=False,
            verbose=True
        )

    def cluster_notes(self, notes: List[NoteCluster]) -> List[NoteCluster]:
        """
        Główna metoda klastrująca. Przyjmuje listę obiektów NoteCluster,
        trenuje model i zwraca te same obiekty z uzupełnionym cluster_id.
        """
        if not notes:
            return []

        # 1. Wyciągamy samą treść do klasteryzacji
        texts = [note.content for note in notes]

        # 2. Dopasowanie modelu i transformacja (klasteryzacja)
        # topics to lista ID klastrów dla każdej notatki (-1 oznacza szum/outlier)
        topics, _ = self.model.fit_transform(texts)

        # 3. Aktualizacja obiektów NoteCluster
        for note, topic_id in zip(notes, topics):
            note.cluster_id = int(topic_id)

        return notes

    def get_topic_info(self):
        """Zwraca tabelę z opisami tematów (słowa kluczowe)"""
        return self.model.get_topic_info()

    def reduce_topics(self, notes: List[NoteCluster], nr_topics: int):
        """Opcjonalna metoda do zmniejszenia liczby klastrów po treningu"""
        texts = [note.content for note in notes]
        self.model.reduce_topics(texts, nr_topics=nr_topics)
        
        # Ponownie aktualizujemy ID po redukcji
        new_topics = self.model.topics_
        for note, topic_id in zip(notes, new_topics):
            note.cluster_id = int(topic_id)
        
        return notes