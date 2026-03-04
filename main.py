import streamlit as st
from rag import load_settings

if "rag_settings" not in st.session_state:
    st.session_state.rag_settings = load_settings()

from ui.home import show_home
from ui.ask import show_ask
from ui.voice import show_voice
from ui.upload import show_upload
from ui.documents import show_document
from ui.preview import show_preview
from ui.analysis import show_analysis
from ui.setting import show_setting

st.set_page_config(layout="wide")

if "page" not in st.session_state:
    st.session_state.page = "home"

st.markdown("""
<style>
.navbar-wrapper div[data-testid="column"] > div {
    display: flex;
    align-items: center;
    height: 100px;
}
div[data-testid="stTabs"] {
    margin: 0 !important;
}
/* Tab list */
div[data-baseweb="tab-list"] {
    height: 100px;
    align-items: center !important;
}
/* Tab button */
button[data-baseweb="tab"] {
    height: 100px !important;
    padding: 0 24px !important;
    border-radius: 0 !important;
    font-weight: 500 !important;
}
/* Hover */
button[data-baseweb="tab"]:hover {
    background-color: #f5f5f5 !important;
}
/* Active */
button[data-baseweb="tab"][aria-selected="true"] {
    background-color: #e6f0ff !important;
    font-weight: 600 !important;
    color: #1f77ff !important;
}         
.block-container {
    padding-top: 1rem !important;
}
/* Tab container */
div[data-baseweb="tab-list"] {
    display: flex !important;
}
button[data-baseweb="tab"] {
    flex: 1 !important;
    justify-content: center !important;
}
</style>
""", unsafe_allow_html=True)


# Navbar
st.markdown('<div class="navbar-wrapper">', unsafe_allow_html=True)

col_tabs = st.columns([1,7], gap="small")

tabs = st.tabs([
    "Home",
    "Ask",
    "Voice",
    "Upload",
    "Document",
    "Preview",
    "Analysis",
    "Setting",
    ])

st.markdown('</div>', unsafe_allow_html=True)


with tabs[0]:
    show_home()
with tabs[1]:
    show_ask()
with tabs[2]:
    show_voice()
with tabs[3]:
    show_upload()
with tabs[4]:
    show_document()
with tabs[5]:
    show_preview()
with tabs[6]:
    show_analysis()
with tabs[7]:
    show_setting()