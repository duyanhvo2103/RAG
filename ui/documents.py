import streamlit as st
import os
import time
from rag.config import PDF_DIR

def show_document():
    st.set_page_config(
        page_title="RAG Assistant",
        layout="wide", 
        initial_sidebar_state="collapsed"
    )

    st.title("Document Library")

    if not os.path.exists(PDF_DIR):
        os.makedirs(PDF_DIR, exist_ok=True)
    # Get the PDF list
    pdfs = [f for f in os.listdir(PDF_DIR) if f.lower().endswith(".pdf")]
    pdfs.sort()

    if not pdfs:
        st.info("No documents uploaded.")
    else:
        for pdf in pdfs:
            file_path = os.path.join(PDF_DIR, pdf)
            stat = os.stat(file_path)
            file_size_mb = stat.st_size / (1024 * 1024)
            upload_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stat.st_mtime))

            # Layout PDF list
            col1, col2, col3, col4 = st.columns([4, 2, 2, 1])

            with col1:
                st.markdown(f"**{pdf}**")
                st.markdown(f"- Size: {file_size_mb:.2f} MB  ")
                st.markdown(f"- Uploaded: {upload_time}")

            with col2:
                if st.button("Delete", key=f"delete_{pdf}"):
                    os.remove(file_path)
                    st.success(f"Deleted {pdf}")
                    st.rerun()

            st.divider()
