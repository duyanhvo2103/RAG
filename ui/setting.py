import streamlit as st
import json
from rag.config import SETTINGS_FILE
from rag.__init__ import load_settings

def show_setting():
    st.set_page_config(
        page_title="RAG Assistant",
        layout="wide", 
        initial_sidebar_state="collapsed"
    )

    st.title("RAG Settings")

    # Init session_state rag_settings
    if "rag_settings" not in st.session_state:
        st.session_state.rag_settings = load_settings()

    settings = st.session_state.rag_settings

    # Embedding model settings
    st.subheader("Embedding Model")
    settings["embedding_model"] = st.selectbox(
        "Select embedding model:",
        ["sentence-transformers/all-MiniLM-L6-v2"],
        index=["sentence-transformers/all-MiniLM-L6-v2"].index(settings["embedding_model"])
    )

    # Chunking settings
    st.subheader("Document Chunking")
    settings["parent_chunk_size"] = st.number_input(
        "Parent chunk size",
        min_value=100, max_value=5000,
        value=settings["parent_chunk_size"],
        step=100
    )
    settings["parent_chunk_overlap"] = st.number_input(
        "Parent chunk overlap",
        min_value=0, max_value=1000,
        value=settings["parent_chunk_overlap"],
        step=50
    )
    settings["child_chunk_size"] = st.number_input(
        "Child chunk size",
        min_value=50, max_value=2000,
        value=settings["child_chunk_size"],
        step=50
    )
    settings["child_chunk_overlap"] = st.number_input(
        "Child chunk overlap",
        min_value=0, max_value=500,
        value=settings["child_chunk_overlap"],
        step=25
    )

    # Retrieval settings
    st.subheader("Retrieval Settings")
    settings["child_search_limit"] = st.number_input(
        "Child search limit",
        min_value=0, max_value=100,
        value=settings["child_search_limit"],
        step=1
    )
    settings["top_k"] = st.number_input(
        "Number of top results (k)",
        min_value=1, max_value=50,
        value=settings["top_k"],
        step=1
    )

    # Rerank model settings
    st.subheader("Rerank Model")
    settings["rerank_model"] = st.selectbox(
        "Select rerank model:",
        ["cross-encoder/ms-marco-MiniLM-L-6-v2"],
        index=["cross-encoder/ms-marco-MiniLM-L-6-v2"].index(settings["rerank_model"])
    )

    # LLM model settings
    st.subheader("LLM Model")
    settings["llm_model"] = st.selectbox(
        "Select llm model:",
        ["gemini-2.5-flash"],
        index=["gemini-2.5-flash"].index(settings["llm_model"])
    )
    settings["temperature"] = st.number_input(
        "Temperature",
        min_value=0.0, max_value=2.0,
        value=settings["temperature"],
        step=0.1
    )

    # Save & Reset
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Save Settings"):
            st.session_state.rag_settings = settings
            # Save settings to file
            with open(SETTINGS_FILE, "w") as f:
                json.dump(settings, f, indent=2)
            st.success("Settings saved!")

    with col2:
        if st.button("Reset to defaults"):
            st.session_state.rag_settings = {
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
            with open(SETTINGS_FILE, "w") as f:
                json.dump(st.session_state.rag_settings, f, indent=2)
            st.rerun()
            st.success("♻️ Settings reset to defaults!")
            
