"""Answer service for generating LLM-based answers."""

import re
from typing import Optional, List, Dict, Any
from langchain_core.documents import Document
from app.core.domain.database import AnswerDB, INoteRepository
from app.core.domain.vectorstore import IVectorStore
from app.infrastructure.prompts.answer_schema import AnswerSchema
from app.infrastructure.prompts.answer_prompt import ANSWER_PROMPT_TEMPLATE


class AnswerService:
    """Service for generating answers using LLM and vectorstore."""
    
    def __init__(
        self,
        repository: INoteRepository,
        vector_store: IVectorStore,
        llm
    ):
        self.repository = repository
        self.vector_store = vector_store
        self.llm = llm
    
    def generate_answer(
        self,
        query: str,
        user_id: int,
        k: int = 10,
        threshold: float = 0.4
    ) -> AnswerDB:
        """Generate an answer using LLM based on retrieved chunks.
        
        Args:
            query: The user's question
            user_id: The user ID
            k: Maximum number of chunks to retrieve
            threshold: Minimum similarity score threshold
            
        Returns:
            AnswerDB object with generated answer and references
        """
        # Retrieve relevant chunks from vectorstore
        relevant_chunks_with_scores = self.vector_store.retrieve_chunks(
            query, user_id, k=k, threshold=threshold
        )
        
        if not relevant_chunks_with_scores:
            # No relevant chunks found
            answer_db = AnswerDB(
                id=None,
                user_id=user_id,
                question=query,
                answer_text="Nie znaleziono odpowiednich notatek w bazie danych, które mogłyby odpowiedzieć na to pytanie.",
                title="Brak odpowiedzi",
                references={}
            )
            answer_id = self.repository.create_answer(answer_db)
            answer_db.id = answer_id
            return answer_db
        
        # Format chunks as LangChain Documents with numbered context
        documents = []
        references_map = {}  # Maps citation number to reference data
        
        for idx, (chunk_vs, score) in enumerate(relevant_chunks_with_scores, start=1):
            # Create document with citation number
            doc = Document(
                page_content=chunk_vs.content,
                metadata={
                    "chunk_number": idx,
                    "note_id": chunk_vs.id,
                    "chunk_id": chunk_vs.chunk_id,
                    "score": score
                }
            )
            documents.append(doc)
            
            # Store reference mapping
            references_map[str(idx)] = {
                "note_id": chunk_vs.id,
                "chunk_id": chunk_vs.chunk_id,
                "chunk_text": chunk_vs.content
            }
        
        # Format context for prompt
        context_parts = []
        for doc in documents:
            chunk_num = doc.metadata["chunk_number"]
            context_parts.append(f"[{chunk_num}] {doc.page_content}")
        
        context = "\n\n".join(context_parts)
        
        # Create prompt
        prompt = ANSWER_PROMPT_TEMPLATE.format(
            context=context,
            question=query
        )
        
        # Generate answer using LLM with structured output
        try:
            # Bind structured output schema
            structured_llm = self.llm.with_structured_output(AnswerSchema)
            
            # Invoke LLM
            result = structured_llm.invoke(prompt)
            
            title = result.title
            answer_text = result.answer
            
        except Exception as e:
            # Fallback if structured output fails
            import logging
            logging.getLogger(__name__).warning(f"Structured output failed: {e}, using regular output")
            response = self.llm.invoke(prompt)
            answer_text = response.content if hasattr(response, 'content') else str(response)
            title = query[:50] + "..." if len(query) > 50 else query
        
        # Extract citations from answer text and build final references map
        # Find all citation patterns like [1], [2], [1][2], etc.
        citation_pattern = r'\[(\d+)\]'
        citations_found = set(re.findall(citation_pattern, answer_text))
        
        # Sort found citations to create sequential mapping
        sorted_citations = sorted(citations_found, key=int)
        
        # Create mapping: old citation number -> new sequential number (1, 2, 3...)
        citation_mapping = {}  # Maps old citation number to new sequential number
        renumbered_references = {}
        
        for new_num, old_num in enumerate(sorted_citations, start=1):
            if old_num in references_map:
                citation_mapping[old_num] = str(new_num)
                renumbered_references[str(new_num)] = references_map[old_num]
        
        # Replace old citation numbers with new sequential numbers in answer text
        for old_num, new_num in citation_mapping.items():
            answer_text = re.sub(rf'\[{old_num}\]', f'[{new_num}]', answer_text)
        
        # Use renumbered references
        final_references = renumbered_references

        # Create AnswerDB
        answer_db = AnswerDB(
            id=None,
            user_id=user_id,
            question=query,
            answer_text=answer_text,
            title=title,
            references=final_references
        )
        
        # Save to database
        answer_id = self.repository.create_answer(answer_db)
        answer_db.id = answer_id
        
        return answer_db
    
    def get_answer(self, answer_id: int, user_id: int) -> Optional[AnswerDB]:
        """Get an answer by ID, ensuring it belongs to the user."""
        return self.repository.get_answer(answer_id, user_id)
    
    def get_answers_by_user(self, user_id: int) -> List[AnswerDB]:
        """Get all answers for a user."""
        return self.repository.get_answers_by_user(user_id)

