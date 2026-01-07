from abc import ABC, abstractmethod
from typing import List

from app.core.domain.clusterization.note import NoteCluster

class IClusterizer(ABC):
    @abstractmethod
    def cluster_notes(self, notes: List[NoteCluster]) -> List[NoteCluster]:
        pass

    @abstractmethod
    def get_topic_info(self):
        pass

    @abstractmethod
    def reduce_topics(self, notes: List[NoteCluster], nr_topics: int):
        pass