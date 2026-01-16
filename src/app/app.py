"""FastAPI application."""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import auth, notes, groups, query, search, ask


app = FastAPI(
    title="NotepadLM",
    description="Semantic note-taking system with LLM-based features",
    version="0.1.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(notes.router)
app.include_router(groups.router)
app.include_router(query.router)
app.include_router(search.router)
app.include_router(ask.router)


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "NotepadLM API"}

