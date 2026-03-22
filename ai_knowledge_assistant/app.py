import streamlit as st
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from data_loader import PDFLoader
from embeddings import EmbeddingModel
from vector_store import VectorStore
from rag_pipeline import RAGPipeline

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = VectorStore()
    st.session_state.vector_store.load()

if 'embedding_model' not in st.session_state:
    with st.spinner("Loading embedding model..."):
        st.session_state.embedding_model = EmbeddingModel()

if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = RAGPipeline(
        st.session_state.vector_store,
        st.session_state.embedding_model
    )

# Header
st.title("🤖 AI Knowledge Assistant")
st.markdown("**RAG-powered Q&A system using Vector Database**")
st.markdown("---")

# Sidebar for document upload
with st.sidebar:
    st.header("📄 Document Management")
    
    # API Key input - check if already loaded from .env
    env_api_key = os.getenv('GEMINI_API_KEY')
    if env_api_key:
        st.success("✅ API Key loaded from .env file")
        api_key = env_api_key
    else:
        api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API key")
    
    if api_key:
        os.environ['GEMINI_API_KEY'] = api_key
        st.session_state.rag_pipeline = RAGPipeline(
            st.session_state.vector_store,
            st.session_state.embedding_model,
            api_key
        )
    
    st.markdown("---")
    
    # File upload
    uploaded_file = st.file_uploader("Upload PDF", type=['pdf'])
    
    if uploaded_file:
        if st.button("Process PDF"):
            with st.spinner("Processing PDF..."):
                try:
                    # Save uploaded file temporarily
                    temp_path = f"temp_{uploaded_file.name}"
                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Load and process
                    loader = PDFLoader(chunk_size=500, overlap=50)
                    text = loader.load_pdf(temp_path)
                    chunks = loader.chunk_text(text)
                    
                    # Generate embeddings
                    embeddings = st.session_state.embedding_model.encode(chunks)
                    
                    # Store in vector database
                    st.session_state.vector_store.add_vectors(embeddings, chunks)
                    st.session_state.vector_store.save()
                    
                    # Cleanup
                    os.remove(temp_path)
                    
                    st.success(f"✅ Processed {len(chunks)} chunks from {uploaded_file.name}")
                    logger.info(f"Successfully processed {uploaded_file.name}")
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
                    logger.error(f"Error processing PDF: {e}")
    
    st.markdown("---")
    
    # Stats
    st.subheader("📊 Database Stats")
    st.metric("Total Chunks", len(st.session_state.vector_store.vectors))
    
    if st.button("Clear Database"):
        st.session_state.vector_store.clear()
        st.session_state.vector_store.save()
        st.success("Database cleared")
        st.rerun()

# Main area - Query interface
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Ask a Question")
    
    # Query input
    query = st.text_input("Enter your question:", placeholder="What is this document about?")
    
    # Top-k slider
    top_k = st.slider("Number of context chunks to retrieve", 1, 10, 3)
    
    if st.button("Search", type="primary"):
        if not query:
            st.warning("Please enter a question")
        elif len(st.session_state.vector_store.vectors) == 0:
            st.warning("Please upload and process a PDF first")
        else:
            with st.spinner("Searching and generating answer..."):
                result = st.session_state.rag_pipeline.query(query, top_k=top_k)
                
                # Display answer
                st.markdown("### 🎯 Answer")
                st.info(result['answer'])
                
                # Display retrieved context
                st.markdown("### 📚 Retrieved Context")
                for i, ctx in enumerate(result['context'], 1):
                    with st.expander(f"Context {i} (Similarity: {ctx['score']:.4f})"):
                        st.text(ctx['text'])

with col2:
    st.header("ℹ️ About")
    st.markdown("""
    This AI Knowledge Assistant uses:
    
    - **RAG (Retrieval Augmented Generation)** for accurate answers
    - **Vector Database** for semantic search
    - **Sentence Transformers** for embeddings
    - **Gemini API** for answer generation
    
    **How to use:**
    1. Enter your Gemini API key in the sidebar
    2. Upload a PDF document
    3. Click "Process PDF"
    4. Ask questions about the document
    """)
    
    st.markdown("---")
    st.markdown("**Powered by Endee-inspired Vector DB**")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit • Sentence Transformers • Google Gemini")
