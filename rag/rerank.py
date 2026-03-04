# rag/rerank.py
from sentence_transformers import CrossEncoder
from streamlit import session_state as ss

RERANK_MODEL = ss.rag_settings["rerank_model"]

_reranker = None

def get_reranker():
    global _reranker
    if _reranker is None:
        _reranker = CrossEncoder(RERANK_MODEL)
    return _reranker

def rerank(query, parent_docs):
    reranker = get_reranker()
    pairs = [(query, d.page_content) for d in parent_docs]
    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(parent_docs, scores),
        key=lambda x: x[1],
        reverse=True
    )
    return ranked
