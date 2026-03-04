import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance
from langchain_community.embeddings import HuggingFaceEmbeddings
from rag.config import QDRANT_PATH
from streamlit import session_state as ss

_embedding = None
_client = None
EMBED_MODEL = ss.rag_settings["embedding_model"]
COLLECTION_NAME = "regulations"

# Embedding
def get_embedding():
    global _embedding
    if _embedding is None:
        _embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    return _embedding


# QDRANT client (run local)
def get_client():
    """
    Qdrant local disk:
    - F5 Streamlit: data còn
    - Restart app: data reset (OK theo yêu cầu)
    """
    global _client
    if _client is None:
        _client = QdrantClient(path=QDRANT_PATH)
        ensure_collection()
    return _client


# Collection init
def ensure_collection():
    client = _client
    embed = get_embedding()
    vector_size = len(embed.embed_query("test"))

    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION_NAME not in names:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )


# Upsert
def upsert_children(child_docs):
    embed = get_embedding()
    client = get_client()

    texts = [d.page_content for d in child_docs]
    vectors = embed.embed_documents(texts)

    points = [
        PointStruct(
            id=str(uuid.uuid4()),
            vector=v,
            payload=d.metadata
        )
        for d, v in zip(child_docs, vectors)
    ]

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )


# Search
def search_children(query_text, limit=20):
    embed = get_embedding()
    client = get_client()

    vector = embed.embed_query(query_text)

    return client.query_points(
        collection_name=COLLECTION_NAME,
        query=vector,
        limit=limit,
        with_payload=True
    ).points
