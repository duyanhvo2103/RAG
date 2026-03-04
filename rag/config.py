# rag/config.py

PDF_DIR = "data/pdf"
QDRANT_PATH = "data/qdrant"
DOCSTORE_PATH = "data/docstore.pkl"
RERANK_LOG_DIR = "data/analysis"
SETTINGS_FILE = "data/rag_settings.json"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
RERANK_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

PARENT_CHUNK_SIZE = 2000
PARENT_CHUNK_OVERLAP = 200

CHILD_CHUNK_SIZE = 500
CHILD_CHUNK_OVERLAP = 100

CHILD_SEARCH_LIMIT = 20
TOP_K_PARENT = 3
