import streamlit as st
from rag.qa import answer_question

def show_ask():
    st.set_page_config(
        page_title="RAG Assistant",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.title("RAG Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_disabled" not in st.session_state:
        st.session_state.chat_disabled = False

    chat_container = st.container(height=600)

    # Render history
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

                if msg["role"] == "assistant" and msg.get("sources"):
                    with st.expander("Sources"):
                        for idx, src in enumerate(msg["sources"], 1):
                            st.markdown(
                                f"**{idx}.** `{src['file']}` — page {src['page']}"
                            )

        if not st.session_state.chat_disabled:
            user_input = st.chat_input("Ask something about your documents...")

            if user_input:
                st.session_state.chat_disabled = True

                st.session_state.pending_question = user_input

                st.rerun()

        if st.session_state.chat_disabled:
            question = st.session_state.get("pending_question")

            if question:
                st.session_state.messages.append({
                    "role": "user",
                    "content": question
                })

                with st.chat_message("user"):
                    st.markdown(question)

                with st.chat_message("assistant"):
                    with st.spinner("Thinking..."):
                        ans, ranked_parents = answer_question(question)

                sources = [
                    {
                        "file": doc.metadata.get("source", "Unknown"),
                        "page": doc.metadata.get("page_number", "N/A")
                    }
                    for doc, _ in ranked_parents
                ]

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ans,
                    "sources": sources
                })

                st.session_state.chat_disabled = False
                st.session_state.pending_question = None

                st.rerun()
