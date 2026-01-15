from dataclasses import dataclass
from pydantic import Field
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Tuple

@dataclass
class UMAPConfig:
    n_neighbors: int = Field(default=15)
    n_components: int = Field(default=5)
    min_dist: float = Field(default=0.1)
    metric: str = Field(default='cosine')

@dataclass
class HDBSCANConfig:
    min_cluster_size: int = Field(default=10)
    metric: str = Field(default='euclidean')
    prediction_data: bool = Field(default=True)

@dataclass
class VectorizerConfig:
    stop_words: str = Field(default='english')
    ngram_range: Tuple[int, int] = Field(default=(1, 2))
    min_df: int = Field(default=2)
    max_df: float = Field(default=0.90)

@dataclass
class BERTopicConfig:
    min_topic_size: int = Field(default=5)
    top_n_words: int = Field(default=20)
    representation_model: ChatGoogleGenerativeAI = Field(default=None)
    calculate_probabilities: bool = Field(default=False)
    verbose: bool = Field(default=True)

@dataclass
class ClusterizerConfig:
    umap_config: UMAPConfig
    hdbscan_config: HDBSCANConfig
    vectorizer_config: VectorizerConfig
    bertopic_config: BERTopicConfig