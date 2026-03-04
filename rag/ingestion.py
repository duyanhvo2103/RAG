# rag/ingestion.py
import os, uuid
from PyPDF2 import PdfReader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.config import *
from utils.pdf_utils import clean_pdf_text
from rag.vectorstore import upsert_children
from rag.docstore import save_parents
from streamlit import session_state as ss

PARENT_CHUNK_SIZE = ss.rag_settings["parent_chunk_size"]
PARENT_CHUNK_OVERLAP = ss.rag_settings["parent_chunk_overlap"]
CHILD_CHUNK_SIZE = ss.rag_settings["child_chunk_size"]
CHILD_CHUNK_OVERLAP = ss.rag_settings["child_chunk_overlap"]

# PDF processing and document splitting
def ingest_pdf(pdf_path: str):
    reader = PdfReader(pdf_path)
    source = os.path.basename(pdf_path)

    page_docs = []
    for i, page in enumerate(reader.pages):
        text = clean_pdf_text(page.extract_text())
        if text:
            page_docs.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": source,
                        "page_number": i + 1
                    }
                )
            )

    parent_splitter = RecursiveCharacterTextSplitter(
        chunk_size=PARENT_CHUNK_SIZE,
        chunk_overlap=PARENT_CHUNK_OVERLAP
    )

    child_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHILD_CHUNK_SIZE,
        chunk_overlap=CHILD_CHUNK_OVERLAP
    )

    parents = parent_splitter.split_documents(page_docs)

    parent_store = {}
    child_docs = []

    # Metadata processing
    for idx, parent in enumerate(parents):
        pid = str(uuid.uuid4())
        parent.metadata.update({
            "parent_id": pid,
            "parent_index": idx + 1
        })
        parent_store[pid] = parent

        children = child_splitter.create_documents([parent.page_content])
        for cidx, c in enumerate(children):
            c.metadata = {
                "parent_id": pid,
                "source": source,
                "chunk_index": cidx
            }
            child_docs.append(c)

    upsert_children(child_docs)
    save_parents(parent_store)

    return len(parent_store), len(child_docs)
