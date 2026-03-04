import streamlit as st
from rag.qa import answer_question

def show_ask():
    st.set_page_config(
        page_title="RAG Assistant",
        layout="wide", 
        initial_sidebar_state="collapsed"
    )

    st.title("RAG Assistant")

    # Session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            # Hiển thị sources nếu có
            if msg["role"] == "assistant" and "sources" in msg:
                with st.expander("Sources"):
                    for idx, src in enumerate(msg["sources"], 1):
                        st.markdown(
                            f"**{idx}.** `{src['file']}` — page {src['page']}"
                        )

    # Chat input
    q = st.chat_input("Ask something about your documents...")

    if q:
        # Show user message
        st.session_state.messages.append({
            "role": "user",
            "content": q
        })

        with st.chat_message("user"):
            st.markdown(q)

        # Assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                ans, ranked_parents = answer_question(q)

            st.markdown(ans)

            sources = []
            for doc, score in ranked_parents:
                sources.append({
                    "file": doc.metadata.get("source", "Unknown"),
                    "page": doc.metadata.get("page_number", "N/A")
                })

            if sources:
                with st.expander("Sources"):
                    for idx, src in enumerate(sources, 1):
                        st.markdown(
                            f"**{idx}.** `{src['file']}` — page {src['page']}"
                        )

        st.session_state.messages.append({
            "role": "assistant",
            "content": ans,
            "sources": sources
        })
