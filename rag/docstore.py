# rag/docstore.py
import pickle
import os
from rag.config import DOCSTORE_PATH

def save_parents(new_parents: dict):
    store = load_parents()
    store.update(new_parents)
    with open(DOCSTORE_PATH, "wb") as f:
        pickle.dump(store, f)

def load_parents() -> dict:
    if not os.path.exists(DOCSTORE_PATH):
        return {}
    with open(DOCSTORE_PATH, "rb") as f:
        return pickle.load(f)

# QUERY
def get_parent(parent_id):
    store = load_parents()
    return store.get(parent_id)


def get_parents_by_source(source_name: str):
    store = load_parents()
    parents = [
        doc for doc in store.values()
        if doc.metadata.get("source") == source_name
    ]

    return sorted(
        parents,
        key=lambda d: d.metadata.get("parent_index", 0)
    )
