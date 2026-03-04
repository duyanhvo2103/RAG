import streamlit as st
import os
from PIL import Image
from rag.config import PDF_DIR
from rag.docstore import get_parents_by_source
import fitz  # PyMuPDF

def show_preview():
    st.set_page_config(
        page_title="RAG Assistant",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.title("Document Library")

    # State management
    if "selected_file" not in st.session_state:
        st.session_state.selected_file = None
    if "page_key" not in st.session_state:
        st.session_state.page_key = 1
    if "page_idx" not in st.session_state:
        st.session_state.page_idx = 0
    if "parent_expanded" not in st.session_state:
        st.session_state.parent_expanded = None

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
                if st.button("Select", key=f"select_{pdf}"):
                    st.session_state.selected_file = pdf
                    st.session_state.page_key = 1
                    st.session_state.page_idx = 0
                    st.session_state.parent_expanded = None
                    st.rerun()

    if st.session_state.selected_file is None:
        list_pdfs()

    else:
        selected_file = st.session_state.selected_file
        pdf_path = os.path.join(PDF_DIR, selected_file)
        if not os.path.exists(pdf_path):
            st.error(f"PDF not found: {selected_file}")
            st.session_state.selected_file = None
            st.stop()

        st.header(f"Preview: {selected_file}")

        st.markdown("---")
        if st.button("⬅ Back to Document List"):
            st.session_state.selected_file = None
            st.session_state.page_key = 1
            st.session_state.page_idx = 0
            st.session_state.parent_expanded = None
            st.rerun()

        parents = get_parents_by_source(selected_file)
        seen = set()
        unique_parents = []
        for i, parent in enumerate(parents):
            pid = parent.metadata.get("parent_id", i)
            if pid not in seen:
                seen.add(pid)
                unique_parents.append(parent)

        col_pdf, col_chunks = st.columns([2.5, 1.5])

        # Display PDF content
        with col_pdf:
            st.subheader("PDF Preview")
            doc = fitz.open(pdf_path)
            total_pages = len(doc)

            nav1, nav2, nav3 = st.columns([1, 2, 1])
            with nav1:
                if st.button("⬅ Prev"):
                    st.session_state.page_idx = max(0, st.session_state.page_idx - 1)
            with nav3:
                if st.button("Next ➡"):
                    st.session_state.page_idx = min(total_pages - 1, st.session_state.page_idx + 1)

            page = doc[st.session_state.page_idx]
            pix = page.get_pixmap(dpi=120)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            st.image(
                img,
                caption=f"Page {st.session_state.page_idx + 1} / {total_pages}",
                width=600
            )

        # Display parent chunks
        with col_chunks:
            st.subheader("Parent Chunks")
            st.markdown("<div style='margin-top: 50px;'></div>", unsafe_allow_html=True)
            container = st.container(height=850)

            container.markdown('<div class="scroll-container">', unsafe_allow_html=True)

            for i, parent in enumerate(unique_parents):
                parent_id = parent.metadata.get("parent_id", i)
                label = f"Parent #{parent.metadata['parent_index']} (page {parent.metadata['page_number']})"
                key = f"{selected_file}_{parent_id}"

                if "parent_expanded" not in st.session_state:
                    st.session_state.parent_expanded = None

                if container.button(label, key=key):
                    # Page navigation by parent
                    st.session_state.page_idx = parent.metadata['page_number'] - 1

                    # Open or close expanded parent chunks content
                    if st.session_state.parent_expanded == parent_id:
                        st.session_state.parent_expanded = None
                    else:
                        st.session_state.parent_expanded = parent_id
                    st.rerun()


                if st.session_state.parent_expanded == parent_id:
                    container.text(parent.page_content[:500])

            container.markdown('</div>', unsafe_allow_html=True)

