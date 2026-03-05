# Advanced RAG System with Hierarchical Retrieval, Re-ranking & Streamlit UI

A production-oriented **Retrieval-Augmented Generation (RAG)** system featuring:

- Hierarchical chunking (Parent–Child design)
- Local vector database using Qdrant
- Cross-encoder re-ranking
- Strict grounded answering (anti-hallucination)
- Transparent retrieval logging
- Streamlit-based interactive UI
## Demo project: [Website](https://duyanh-rag.streamlit.app/)
---

## 1. Project Overview

This project implements an advanced **RAG pipeline** optimized for:

- High-precision document retrieval  
- Hallucination control  
- Hierarchical document structuring  
- Configurable chunking strategy  
- Local vector storage  
- Transparent re-ranking analysis  

Users can upload PDF documents and ask questions grounded **strictly in the uploaded content**.

---

## 2. Architecture Overview
```bash
PDF → Parent Chunking → Child Chunking → Embedding → Qdrant
                                                   ↓
User Query → Embed → Child Retrieval → Parent Mapping
                                      ↓
                                  Re-ranking
                                      ↓
                                 Context Builder
                                      ↓
                                Gemini LLM Answer
```

---

## 3. Key Features

### 3.1 Hierarchical Chunking Strategy (Parent–Child)

Instead of flat chunking, the system uses a two-level retrieval design:

- **Parent Chunks** → Stored in a local docstore (pickle)
- **Child Chunks** → Embedded & stored in Qdrant
- Retrieval happens at **child level → aggregated back to parent**

#### Benefits

- Better semantic granularity  
- More precise retrieval  
- Reduced context noise  
- Higher grounding accuracy  

---

### 3.2 Local Vector Database (Qdrant)

- Runs locally (disk mode)
- Auto-creates collection if missing
- Uses cosine similarity
- Resets on full app restart (by design)

**Tech stack:**

- `qdrant-client`
- `HuggingFaceEmbeddings`

---

### 3.3 Cross-Encoder Re-ranking

Initial vector search retrieves candidates → then refined using:

        SentenceTransformers CrossEncoder

#### Benefits

- Improved ranking precision  
- Reduced semantic mismatch  
- Better top-k selection  

Re-ranking results are logged into JSON files for transparency.

---

### 3.4 Strict Grounded Answering (Anti-Hallucination)

The LLM is strictly instructed to:

- Use **ONLY** provided context  
- Avoid inference or external knowledge  
- Respond with:

```bash
"I don't know based on the provided context."
```

if unsupported.

#### Suitable for:

- Legal documents  
- Regulations  
- Compliance  
- Enterprise QA  

---

### 3.5 Configurable RAG Settings (Runtime)

All critical parameters are controlled via `session_state`:

| Setting              | Purpose                         |
|----------------------|---------------------------------|
| parent_chunk_size    | Large semantic grouping         |
| child_chunk_size     | Fine-grained retrieval          |
| child_search_limit   | Initial retrieval size          |
| top_k                | Final reranked parents          |
| embedding_model      | HF embedding model              |
| rerank_model         | CrossEncoder model              |
| llm_model            | Gemini model                    |
| temperature          | LLM creativity control          |

Allows live experimentation **without code changes**.

---

## 4. Project Structure
```bash
data/
├── analysis/
├── pdf/
├── qdrant/
├── rag_settings.json
static/
utils/
├── pdf_utils.py
rag/
├── __init__.py
├── ingestion.py # PDF processing & hierarchical chunking
├── retrieval.py # Child search → Parent aggregation
├── rerank.py # CrossEncoder re-ranking
├── qa.py # Context building + LLM answering
├── vectorstore.py # Qdrant + embeddings
├── docstore.py # Parent document persistence
├── config.py # Paths & configuration
│
ui/
├── home.py
├── upload.py
├── ask.py
├── preview.py
├── documents.py
├── analysis.py
├── setting.py
├── voice.py
main.py
requirements.txt
README.md
```

---

## 5. Technical Stack

| Component        | Technology |
|------------------|------------|
| LLM              | Google Gemini (`langchain_google_genai`) |
| Embeddings       | HuggingFace Transformers |
| Vector Database  | Qdrant (local disk mode) |
| Re-ranking       | SentenceTransformers CrossEncoder |
| Framework        | Streamlit |
| PDF Processing   | PyPDF2 |
| Chunking         | RecursiveCharacterTextSplitter (LangChain) |

---

## 6. Core Pipeline Explained

### 6.1 Ingestion

- Extract text from PDF  
- Clean text  
- Split into parent chunks  
- Split parent into child chunks  
- Embed children  
- Store:
  - Children → Qdrant  
  - Parents → Local pickle store  

---

### 6.2 Retrieval

- Embed query  
- Search top-N child chunks  
- Map children → parent IDs  
- Deduplicate parents  

---

### 6.3 Re-ranking

- Use CrossEncoder on `(query, parent_chunk)`  
- Sort by relevance score  
- Keep top-k parents  
- Save ranking logs  

---

### 6.4 Answer Generation

- Construct strict grounding prompt  
- Inject reranked parent content  
- Call Gemini  
- Handle:
  - Quota errors (429)
  - Resource exhaustion
  - Timeout
  - Unexpected failures  

System returns user-friendly messages instead of crashing.

---

## 7. Error Handling

LLM-related errors handled gracefully:

- Quota exhausted  
- Resource exhausted  
- Timeout  
- Generic exceptions  

Ensures production robustness.

---

## 8. Analysis & Transparency

Each query stores logs in:

```bash
rerank_logs/
    rerank_YYYYMMDD_HHMMSS.json
```

Includes:

- Query  
- Parent ID  
- Page number  
- Re-ranking score  

### Enables:

- Retrieval debugging  
- Ranking inspection  
- Evaluation experiments  

---


## 8. Why This Project Stands Out

This is NOT a basic RAG demo.

It demonstrates:

* Hierarchical retrieval design

* Hybrid dense retrieval + cross-encoder ranking

* Controlled hallucination

* Transparent logging

* Configurable experimentation

* Clean separation of responsibilities

* Production-aware error handling

It reflects understanding of:

* Information retrieval theory

* Embedding vs cross-encoder trade-offs

* Context window optimization

* Practical LLM limitations

* System design thinking

## 9. Potential Improvements (Future Work)

* Hybrid BM25 + Dense retrieval

* Metadata filtering

* Multi-query expansion

* Evaluation framework (RAGAS)

* Streaming responses

* Docker deployment

* Persistent Qdrant server mode

* Authentication system for multi-user usage

# Author

Duy Anh

AI Engineer | RAG Systems | LLM Applications
