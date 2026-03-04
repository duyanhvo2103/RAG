# rag/retrieval.py
from rag.vectorstore import search_children
from rag.docstore import get_parent
from streamlit import session_state as ss

CHILD_SEARCH_LIMIT = ss.rag_settings["child_search_limit"]

def retrieve_parents(query_text):
    results = search_children(query_text, limit=CHILD_SEARCH_LIMIT)

    parent_scores = {}
    for r in results:
        pid = r.payload.get("parent_id")
        if pid:
            parent_scores[pid] = max(parent_scores.get(pid, 0), r.score)

    parents = []
    for pid in parent_scores:
        doc = get_parent(pid)
        if doc:
            parents.append(doc)

    return parents
