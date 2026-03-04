import streamlit as st
import os
from rag.ingestion import ingest_pdf
from rag.config import PDF_DIR

def show_upload():
    st.set_page_config(
        page_title="RAG Assistant",
        layout="wide", 
        initial_sidebar_state="collapsed"
    )
    
    st.title("Upload PDF")

    file = st.file_uploader("Upload PDF", type=["pdf"])
    if file:
        path = os.path.join(PDF_DIR, file.name)
        with open(path, "wb") as f:
            f.write(file.read())

        if st.button("Process PDF"):
            p, c = ingest_pdf(path)
            st.success(f"File upload successful")
