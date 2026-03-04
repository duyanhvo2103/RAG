# rag/qa.py
from rag.retrieval import retrieve_parents
from rag.rerank import rerank
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from streamlit import session_state as ss
from rag.config import RERANK_LOG_DIR
import os, json
from datetime import datetime
import streamlit as st

TOP_K_PARENT = ss.rag_settings["top_k"]
LLM_MODEL = ss.rag_settings["llm_model"]
TEMPERATURE = ss.rag_settings["temperature"]
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

# load_dotenv()

llm = ChatGoogleGenerativeAI(
    model=LLM_MODEL,
    temperature=TEMPERATURE,
    google_api_key=GOOGLE_API_KEY
)

# Save rerank results to analysis
def save_rerank_results(query, ranked):
    os.makedirs(RERANK_LOG_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(RERANK_LOG_DIR, f"rerank_{ts}.json")

    data = []
    for doc, score in ranked:
        data.append({
            "source": doc.metadata.get("source", ""),
            "page_number": doc.metadata.get("page_number", None),
            "parent_id": doc.metadata.get("parent_id", None),
            "score": float(score)
        })

    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"query": query, "results": data}, f, ensure_ascii=False, indent=2)


def answer_question(query: str):
    parents = retrieve_parents(query)
    if not parents:
        return "No matching information found.", []

    # Re-rank parent docs
    ranked = rerank(query, parents)
    ranked = ranked[:TOP_K_PARENT]
    save_rerank_results(query, ranked)

    top_docs = [d.page_content for d, _ in ranked]
    context = "\n\n---\n\n".join(top_docs)

    prompt = f"""
        You are a RAG-based assistant. Your task is to answer the question strictly from the provided context.

        Rules:
        - Use ONLY the information explicitly stated in the context.
        - Do NOT infer, guess, or rely on prior knowledge.
        - If the answer is not explicitly supported by the context, respond exactly:
        "I don't know based on the provided context."
        - Answer in the same language as the question.
        - Keep the answer concise and factual.

        Context:
        ---------------------
        {context}
        ---------------------

        Question:
        {query}

        Final Answer:
        """

    try:
        response = llm.invoke(prompt)
        answer = response.content

    # Quota / rate limit
    except Exception as e:
        error_msg = str(e).lower()

        if "quota" in error_msg or "429" in error_msg or "resource_exhausted" in error_msg:
            answer = "The system is temporarily out of quota. Please try again later."
        elif "timeout" in error_msg:
            answer = "The request timed out. Please try again."
        else:
            answer = "An unexpected error occurred. Please try again later."

        print("LLM ERROR:", e)

    return answer, ranked

