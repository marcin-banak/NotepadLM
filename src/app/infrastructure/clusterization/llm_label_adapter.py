import random
from typing import List, Dict
from bertopic.representation import BaseRepresentation


class LLMLabelAdapter(BaseRepresentation):
    def __init__(
        self,
        llm_callable,
        prompt: str,
        max_docs: int = 5,
        max_length: int = 1_000,
        seed: int | None = None,
    ):
        """
        llm_callable: funkcja str -> str
        prompt: prompt z [KEYWORDS] i [DOCUMENTS]
        max_docs: maksymalna liczba dokumentów
        max_length: maksymalna liczba znaków w jednym dokumencie
        seed: opcjonalne ziarno losowości (reprodukowalność)
        """
        self.llm = llm_callable
        self.prompt = prompt
        self.max_docs = max_docs
        self.max_length = max_length
        self.random = random.Random(seed)

    def __call__(
        self,
        topics: List[int],
        documents: List[List[str]],
        keywords: List[List[str]],
    ) -> Dict[int, List[str]]:
        representations = {}

        for topic_id, docs, kws in zip(topics, documents, keywords):
            if not docs or not kws:
                representations[topic_id] = "Unnamed Topic"
                continue

            docs_sample = self._sample_documents(docs)

            prompt = (
                self.prompt
                .replace("[DOCUMENTS]", "\n\n".join(docs_sample))
                .replace("[KEYWORDS]", ", ".join(kws))
            )

            label = self.llm(prompt)
            representations[topic_id] = label.strip()

        return representations

    def _sample_documents(self, docs: List[str]) -> List[str]:
        if not docs:
            return []

        # 1. Wybierz losowo max_docs dokumentów
        selected_docs = (
            self.random.sample(docs, k=min(self.max_docs, len(docs)))
            if len(docs) > self.max_docs
            else docs
        )

        # 2. Z każdego dokumentu weź losowy, spójny fragment
        sampled_chunks: List[str] = []
        for doc in selected_docs:
            if len(doc) <= self.max_length:
                sampled_chunks.append(doc)
                continue

            start = self.random.randint(0, len(doc) - self.max_length)
            chunk = doc[start : start + self.max_length]
            sampled_chunks.append(chunk)

        return sampled_chunks
