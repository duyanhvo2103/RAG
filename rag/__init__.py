# rag/__init__.py
import json
import streamlit as st

from rag.config import SETTINGS_FILE

def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except:
        # If the file does not exist or is corrupted, return to default.
        return {
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "parent_chunk_size": 1000,
            "parent_chunk_overlap": 100,
            "child_chunk_size": 300,
            "child_chunk_overlap": 50,
            "child_search_limit": 20,
            "top_k": 3,
            "vectorstore_mode": "in-memory",
            "llm_model": "gemini-2.5-flash",
            "rerank_model": "cross-encoder/ms-marco-MiniLM-L-6-v2",
            "temperature": 0.5
        }