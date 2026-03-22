"""
Example script demonstrating programmatic usage of the AI Knowledge Assistant
without the Streamlit UI
"""
import os
import logging
from data_loader import PDFLoader
from embeddings import EmbeddingModel
from vector_store import VectorStore
from rag_pipeline import RAGPipeline

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Example usage of the RAG system."""
    
    # Set your API key
    os.environ['GEMINI_API_KEY'] = 'your_api_key_here'
    
    # Initialize components
    logger.info("Initializing components...")
    embedding_model = EmbeddingModel()
    vector_store = VectorStore(storage_path='./example_db')
    rag_pipeline = RAGPipeline(vector_store, embedding_model)
    
    # Load and process a PDF
    pdf_path = 'sample.pdf'  # Replace with your PDF path
    
    if os.path.exists(pdf_path):
        logger.info(f"Processing PDF: {pdf_path}")
        
        # Load PDF
        loader = PDFLoader(chunk_size=500, overlap=50)
        text = loader.load_pdf(pdf_path)
        chunks = loader.chunk_text(text)
        
        logger.info(f"Created {len(chunks)} chunks")
        
        # Generate embeddings
        embeddings = embedding_model.encode(chunks)
        
        # Store in vector database
        vector_store.add_vectors(embeddings, chunks)
        vector_store.save()
        
        logger.info("PDF processed and stored in vector database")
    else:
        logger.info("No PDF found. Loading existing vector store...")
        vector_store.load()
    
    # Query the system
    questions = [
        "What is the main topic of this document?",
        "Can you summarize the key points?",
        "What are the important findings?"
    ]
    
    for question in questions:
        logger.info(f"\nQuestion: {question}")
        result = rag_pipeline.query(question, top_k=3)
        
        print(f"\n{'='*60}")
        print(f"Question: {result['query']}")
        print(f"{'='*60}")
        print(f"\nAnswer:\n{result['answer']}")
        print(f"\nRetrieved Context:")
        for i, ctx in enumerate(result['context'], 1):
            print(f"\n[{i}] Similarity: {ctx['score']:.4f}")
            print(f"{ctx['text'][:200]}...")
        print(f"\n{'='*60}\n")

if __name__ == "__main__":
    main()
