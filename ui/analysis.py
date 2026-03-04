import streamlit as st
import os
import json
from PIL import Image
import fitz
from rag.config import PDF_DIR, RERANK_LOG_DIR

def show_analysis():
    st.set_page_config(
        page_title="RAG Assistant",
        layout="wide", 
        initial_sidebar_state="collapsed"
    )

    st.title("Document Coverage")

    if "selected_cov_file" not in st.session_state:
        st.session_state.selected_cov_file = None
    if "page_usage_cache" not in st.session_state:
        st.session_state.page_usage_cache = {}

    def show_pdf_scroll(pdf_path, dpi=100):
        doc = fitz.open(pdf_path)

        for i in range(len(doc)):
            page = doc[i]
            pix = page.get_pixmap(dpi=dpi)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            st.image(
                img,
                caption=f"Page {i + 1} / {len(doc)}",
                width=500
            )

    def list_pdfs():
        pdfs = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]
        pdfs.sort()
        if not pdfs:
            st.info("No documents uploaded.")
            return
        st.subheader("Available PDFs")
        for pdf in pdfs:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"**{pdf}**")
            with col2:
                if st.button("Select", key=f"cov_select_{pdf}"):
                    st.session_state.selected_cov_file = pdf
                    st.rerun()

    if st.session_state.selected_cov_file is None:
        list_pdfs()

    # Show coverage analysis
    else:
        selected_cov_pdf = st.session_state.selected_cov_file
        pdf_path = os.path.join(PDF_DIR, selected_cov_pdf)
        if not os.path.exists(pdf_path):
            st.error(f"PDF not found: {selected_cov_pdf}")
            st.session_state.selected_cov_file = None
            st.stop()

        st.header(f"Coverage Analysis: {selected_cov_pdf}")

        st.markdown("---")
        if st.button("⬅ Back to PDF list"):
            st.session_state.selected_cov_file = None
            st.rerun()

        # Load page usage from rerank logs
        if selected_cov_pdf in st.session_state.page_usage_cache:
            page_usage = st.session_state.page_usage_cache[selected_cov_pdf]
        else:
            page_usage = {}
            for fname in os.listdir(RERANK_LOG_DIR):
                if fname.endswith(".json"):
                    path = os.path.join(RERANK_LOG_DIR, fname)
                    try:
                        with open(path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            for item in data.get("results", []):
                                source = item.get("source", "")
                                page = item.get("page_number")
                                if page is not None and source == selected_cov_pdf:
                                    page_usage[page] = page_usage.get(page, 0) + 1
                    except Exception:
                        continue
            st.session_state.page_usage_cache[selected_cov_pdf] = page_usage

        if not page_usage:
            st.info("No retrieval data found for this PDF.")
        else:
            # Show top pages
            st.subheader("Top retrieved pages")
            sorted_pages = sorted(page_usage.items(), key=lambda x: x[1], reverse=True)
            max_count = max(page_usage.values()) if page_usage else 1

            for page, count in sorted_pages:
                col1, col2 = st.columns([1, 4])
                col1.markdown(f"Page {page}")
                col2.progress(count / max_count)
                col2.markdown(f"{count} times")

