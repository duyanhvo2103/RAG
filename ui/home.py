# home.py
import streamlit as st

def show_home():
    st.set_page_config(
        page_title="PDF RAG QA",
        layout="wide",
        initial_sidebar_state="collapsed"
    )


    st.markdown("""
        <style>
        .hero {
            padding: 20px 20px 60px 20px;
            text-align: center;
        }
        .hero-title {
            font-size: 52px;
            font-weight: 800;
            margin-bottom: 20px;
        }
        .gradient-text {
            background: linear-gradient(90deg, #3b82f6, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
            font-size: 20px;
            color: #9aa0a6;
            max-width: 800px;
            margin: auto;
            line-height: 1.6;
        }
        .section-title {
            text-align: center;
            font-size: 30px;
            font-weight: 700;
            margin-top: 80px;
            margin-bottom: 40px;
        }
        .feature-card {
            background-color: #111827;
            padding: 30px;
            border-radius: 14px;
            border: 1px solid #1f2937;
            transition: 0.3s;
            height: 100%;
        }
        .feature-card:hover {
            border: 1px solid #3b82f6;
            transform: translateY(-6px);
        }
        .feature-title {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 15px;
        }
        .metrics {
            text-align: center;
            font-size: 28px;
            font-weight: 700;
        }
        .metric-label {
            font-size: 14px;
            color: #9aa0a6;
        }
        .footer {
            text-align: center;
            color: #6b7280;
            font-size: 14px;
            margin-top: 100px;
            padding-bottom: 30px;
        }
        </style>
    """, unsafe_allow_html=True)


    # Hero Section
    st.markdown("""
        <div class="hero">
            <div class="hero-title">
                📄 <span class="gradient-text">Intelligent PDF Assistant</span>
            </div>
            <div class="hero-subtitle">
                A Retrieval-Augmented Generation (RAG) system designed to transform 
                static PDF documents into dynamic, searchable, AI-powered knowledge.
                <br><br>
                Upload. Retrieve. Analyze. Ask. Understand.
            </div>
        </div>
    """, unsafe_allow_html=True)


    st.markdown("""
    <style>
    .metric-box {
        text-align: center;
        padding: 20px 10px;
        border-radius: 12px;
        background-color: #00008b;
        height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .metric-title {
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 6px;
    }
    .metric-label {
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-title">⚡ Fast</div>
            <div class="metric-label">Optimized Retrieval Pipeline</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-title">🎯 Accurate</div>
            <div class="metric-label">Semantic + Rerank Strategy</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-title">🧠 Context-Aware</div>
            <div class="metric-label">LLM Grounded Answers</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="metric-box">
            <div class="metric-title">⚙ Customizable</div>
            <div class="metric-label">Flexible Configuration</div>
        </div>
        """, unsafe_allow_html=True)


    # Core Capabilities
    st.markdown('<div class="section-title">Core Capabilities</div>', unsafe_allow_html=True)

    colA, colB, colC = st.columns(3)

    with colA:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">📥 Smart Document Processing</div>
                • Parent–Child chunking strategy<br>
                • Configurable chunk size & overlap<br>
                • Efficient indexing pipeline<br><br>
                Designed for structured and scalable knowledge ingestion.
            </div>
        """, unsafe_allow_html=True)

    with colB:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">🔎 Advanced Retrieval Engine</div>
                • Embedding-based semantic search<br>
                • Adjustable top-k retrieval<br>
                • Cross-encoder reranking support<br><br>
                Ensures highly relevant context selection before generation.
            </div>
        """, unsafe_allow_html=True)

    with colC:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-title">🤖 AI-Powered Answer Generation</div>
                • Context-grounded responses<br>
                • Configurable LLM models<br>
                • Temperature control<br><br>
                Produces reliable, explainable answers directly from documents.
            </div>
        """, unsafe_allow_html=True)


    st.markdown("""
    <style>
    .section-title {
        font-size: 28px;
        font-weight: 700;
        margin-top: 40px;
        margin-bottom: 20px;
    }
    .workflow-card {
        background: #111827;
        padding: 20px;
        border-radius: 14px;
        margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transition: 0.2s ease-in-out;
    }
    .workflow-card:hover {
        transform: translateY(-4px);
    }
    .workflow-step {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .workflow-desc {
        font-size: 14px;
        color: #555;
    }
    .config-box {
        background: linear-gradient(135deg, #eef2ff, #f8f9ff);
        padding: 25px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .config-title {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 15px;
    }
    .config-item {
        margin-bottom: 8px;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)


    # Workflow Section
    st.markdown('<div class="section-title">⚙ System Workflow</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-step">1️⃣ Upload PDF</div>
            <div class="workflow-desc">Import your document into the system.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-step">2️⃣ Embedding & Indexing</div>
            <div class="workflow-desc">Convert text into vector representations and store efficiently.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-step">3️⃣ Semantic Retrieval</div>
            <div class="workflow-desc">Identify the most relevant document segments.</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-step">4️⃣ Reranking (Optional)</div>
            <div class="workflow-desc">Improve ranking precision with cross-encoder models.</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="workflow-card">
            <div class="workflow-step">5️⃣ LLM Response Generation</div>
            <div class="workflow-desc">Produce a grounded answer using retrieved context.</div>
        </div>
        """, unsafe_allow_html=True)


    # Configuration Section
    st.markdown("""
    <style>
    .config-container {
        background: #111827;
        padding: 30px;
        border-radius: 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.06);
        margin-top: 20px;
    }
    .config-header {
        text-align: center;
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .config-subtext {
        font-size: 14px;
        color: #555;
        margin-bottom: 25px;
    }
    .config-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 15px 40px;
    }
    .config-item {
        display: flex;
        align-items: center;
        font-size: 17px;
        padding: 10px 0;
        font-weight: 600;
    }
    .config-icon {
        font-size: 18px;
        margin-right: 10px;
    }
    .config-footer {
        margin-top: 25px;
        font-size: 13px;
        color: #444;
        opacity: 0.8;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="config-container">

    <div class="config-header">🛠 Flexible Configuration</div>
    <div class="config-subtext">
    Fine-tune every stage of the retrieval and generation pipeline.
    </div>

    <div class="config-grid">

    <div class="config-item"><span class="config-icon">🔎</span>Embedding model selection</div>
    <div class="config-item"><span class="config-icon">🧩</span>Parent & child chunk parameters</div>

    <div class="config-item"><span class="config-icon">📊</span>Retrieval limits</div>
    <div class="config-item"><span class="config-icon">🎯</span>Reranking model configuration</div>

    <div class="config-item"><span class="config-icon">🤖</span>LLM model selection</div>
    <div class="config-item"><span class="config-icon">🌡️</span>Temperature tuning</div>

    </div>

    <div class="config-footer">
    Designed for research environments, enterprise deployment, and internal knowledge systems.
    </div>

    </div>
    """, unsafe_allow_html=True)


    st.markdown('<div class="section-title">Get Started</div>', unsafe_allow_html=True)

    st.markdown("""
    <style>
    .center-wrapper {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    .success-box {
        background-color: #008000;
        padding: 18px 24px;
        border-radius: 12px;
        font-weight: 500;
        width: 80%;
        text-align: center;
        border: 1px solid #b7e1c1;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="center-wrapper">
        <div class="success-box">
            Use the navigation menu to upload a document and begin exploring your AI-powered knowledge system.
        </div>
    </div>
    """, unsafe_allow_html=True)


    # Footer
    st.markdown("""
        <div class="footer">
            PDF RAG QA System • Built with Streamlit • Retrieval-Augmented Generation Architecture
        </div>
    """, unsafe_allow_html=True)