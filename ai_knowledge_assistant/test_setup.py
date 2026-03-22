"""
Test script to verify the AI Knowledge Assistant setup
"""
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_imports():
    """Test if all required modules can be imported."""
    logger.info("Testing imports...")
    try:
        import streamlit
        logger.info("✓ Streamlit imported")
        
        import sentence_transformers
        logger.info("✓ Sentence Transformers imported")
        
        import PyPDF2
        logger.info("✓ PyPDF2 imported")
        
        import numpy
        logger.info("✓ NumPy imported")
        
        import google.generativeai
        logger.info("✓ Google Generative AI imported")
        
        return True
    except ImportError as e:
        logger.error(f"✗ Import failed: {e}")
        return False

def test_modules():
    """Test if custom modules work correctly."""
    logger.info("\nTesting custom modules...")
    try:
        from embeddings import EmbeddingModel
        logger.info("✓ EmbeddingModel imported")
        
        from vector_store import VectorStore
        logger.info("✓ VectorStore imported")
        
        from data_loader import PDFLoader
        logger.info("✓ PDFLoader imported")
        
        from rag_pipeline import RAGPipeline
        logger.info("✓ RAGPipeline imported")
        
        return True
    except Exception as e:
        logger.error(f"✗ Module test failed: {e}")
        return False

def test_embedding_model():
    """Test embedding model initialization."""
    logger.info("\nTesting embedding model...")
    try:
        from embeddings import EmbeddingModel
        model = EmbeddingModel()
        
        # Test encoding
        test_text = "This is a test sentence."
        embedding = model.encode_single(test_text)
        
        logger.info(f"✓ Embedding generated. Dimension: {len(embedding)}")
        return True
    except Exception as e:
        logger.error(f"✗ Embedding test failed: {e}")
        return False

def test_vector_store():
    """Test vector store operations."""
    logger.info("\nTesting vector store...")
    try:
        import numpy as np
        from vector_store import VectorStore
        
        store = VectorStore(storage_path="./test_db")
        
        # Create test vectors
        test_vectors = np.random.rand(5, 384)
        test_texts = [f"Test document {i}" for i in range(5)]
        
        store.add_vectors(test_vectors, test_texts)
        
        # Test search
        query_vector = np.random.rand(384)
        results = store.search(query_vector, top_k=3)
        
        logger.info(f"✓ Vector store working. Found {len(results)} results")
        
        # Cleanup
        import shutil
        shutil.rmtree("./test_db", ignore_errors=True)
        
        return True
    except Exception as e:
        logger.error(f"✗ Vector store test failed: {e}")
        return False

def main():
    """Run all tests."""
    logger.info("=" * 50)
    logger.info("AI Knowledge Assistant - Setup Verification")
    logger.info("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Module Test", test_modules),
        ("Embedding Model Test", test_embedding_model),
        ("Vector Store Test", test_vector_store)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    logger.info("\n" + "=" * 50)
    logger.info("Test Results:")
    logger.info("=" * 50)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        logger.info(f"{test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        logger.info("\n✓ All tests passed! You're ready to run the application.")
        logger.info("Run: streamlit run app.py")
        return 0
    else:
        logger.error("\n✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
