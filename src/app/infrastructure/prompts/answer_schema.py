"""LangChain schema for structured answer output."""

from typing import Optional
from pydantic import BaseModel, Field


class AnswerSchema(BaseModel):
    """Schema for LLM-generated answer with citations."""
    
    title: str = Field(
        description="A concise, descriptive title for the answer (maximum 10 words)"
    )
    answer: str = Field(
        description="The answer text with citations in format [1][2] where numbers refer to the source chunks provided. "
                   "Use citations whenever you reference information from the provided context."
    )

