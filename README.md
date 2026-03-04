# 🚀 Advanced RAG System with Hierarchical Retrieval, Re-ranking & Streamlit UI

A production-oriented **Retrieval-Augmented Generation (RAG)** system featuring:

- Hierarchical chunking (Parent–Child design)
- Local vector database using Qdrant
- Cross-encoder re-ranking
- Strict grounded answering (anti-hallucination)
- Transparent retrieval logging
- Streamlit-based interactive UI

---

## 📌 Project Overview

This project implements an advanced **RAG pipeline** optimized for:

- 🔎 High-precision document retrieval  
- 🧠 Hallucination control  
- 🏗 Hierarchical document structuring  
- ⚙ Configurable chunking strategy  
- 💾 Local vector storage  
- 📊 Transparent re-ranking analysis  

Users can upload PDF documents and ask questions grounded **strictly in the uploaded content**.

---

## 🧠 Architecture Overview
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

# 🔥 Key Features

## ✅ 1. Hierarchical Chunking Strategy (Parent–Child)

Instead of flat chunking, the system uses a two-level retrieval design:

- **Parent Chunks** → Stored in a local docstore (pickle)
- **Child Chunks** → Embedded & stored in Qdrant
- Retrieval happens at **child level → aggregated back to parent**

### 🎯 Benefits

- Better semantic granularity  
- More precise retrieval  
- Reduced context noise  
- Higher grounding accuracy  

---

## ✅ 2. Local Vector Database (Qdrant)

- Runs locally (disk mode)
- Auto-creates collection if missing
- Uses cosine similarity
- Resets on full app restart (by design)

**Tech stack:**

- `qdrant-client`
- `HuggingFaceEmbeddings`

---

## ✅ 3. Cross-Encoder Re-ranking

Initial vector search retrieves candidates → then refined using:

        SentenceTransformers CrossEncoder

### Benefits

- Improved ranking precision  
- Reduced semantic mismatch  
- Better top-k selection  

Re-ranking results are logged into JSON files for transparency.

---

## ✅ 4. Strict Grounded Answering (Anti-Hallucination)

The LLM is strictly instructed to:

- Use **ONLY** provided context  
- Avoid inference or external knowledge  
- Respond with:

```bash
"I don't know based on the provided context."
```

if unsupported.

### Suitable for:

- Legal documents  
- Regulations  
- Compliance  
- Enterprise QA  

---

## ✅ 5. Configurable RAG Settings (Runtime)

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

# 🗂 Project Structure
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

# ⚙️ Technical Stack

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

# 🧩 Core Pipeline Explained

## 1️⃣ Ingestion

- Extract text from PDF  
- Clean text  
- Split into parent chunks  
- Split parent into child chunks  
- Embed children  
- Store:
  - Children → Qdrant  
  - Parents → Local pickle store  

---

## 2️⃣ Retrieval

- Embed query  
- Search top-N child chunks  
- Map children → parent IDs  
- Deduplicate parents  

---

## 3️⃣ Re-ranking

- Use CrossEncoder on `(query, parent_chunk)`  
- Sort by relevance score  
- Keep top-k parents  
- Save ranking logs  

---

## 4️⃣ Answer Generation

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

# 🛡 Error Handling

LLM-related errors handled gracefully:

- Quota exhausted  
- Resource exhausted  
- Timeout  
- Generic exceptions  

Ensures production robustness.

---

# 📊 Analysis & Transparency

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

# 🚀 How to Run

## 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
```
## 2️⃣ Add Google API Key

In Streamlit secrets:
```bash
GOOGLE_API_KEY = "your_key_here"
```

3️⃣ Run app
```bash
streamlit run app.py
```

# 📈 Why This Project Stands Out

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

# 🎯 Potential Improvements (Future Work)

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