import numpy as np
import pickle
import os
import logging
from typing import List, Tuple, Optional

logger = logging.getLogger(__name__)

class VectorStore:
    """Simulated vector database inspired by Endee architecture."""
    
    def __init__(self, storage_path: str = "./vector_db"):
        self.storage_path = storage_path
        self.vectors = []
        self.metadata = []
        self.dimension = None
        os.makedirs(storage_path, exist_ok=True)
        logger.info(f"Vector store initialized at {storage_path}")
    
    def add_vectors(self, vectors: np.ndarray, texts: List[str]):
        """Store vectors with metadata."""
        if self.dimension is None:
            self.dimension = vectors.shape[1]
        
        for i, (vec, text) in enumerate(zip(vectors, texts)):
            doc_id = len(self.vectors)
            self.vectors.append(vec)
            self.metadata.append({
                'id': doc_id,
                'text': text,
                'chunk_index': i
            })
        logger.info(f"Added {len(vectors)} vectors. Total: {len(self.vectors)}")
    
    def search(self, query_vector: np.ndarray, top_k: int = 5) -> List[Tuple[int, float, str]]:
        """Perform similarity search using cosine similarity."""
        if not self.vectors:
            logger.warning("Vector store is empty")
            return []
        
        vectors_array = np.array(self.vectors)
        
        # Normalize vectors for cosine similarity
        query_norm = query_vector / np.linalg.norm(query_vector)
        vectors_norm = vectors_array / np.linalg.norm(vectors_array, axis=1, keepdims=True)
        
        # Compute cosine similarity
        similarities = np.dot(vectors_norm, query_norm)
        
        # Get top-k indices
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append((
                self.metadata[idx]['id'],
                float(similarities[idx]),
                self.metadata[idx]['text']
            ))
        
        logger.info(f"Search completed. Found {len(results)} results")
        return results
    
    def save(self):
        """Persist vector store to disk."""
        data = {
            'vectors': self.vectors,
            'metadata': self.metadata,
            'dimension': self.dimension
        }
        path = os.path.join(self.storage_path, 'vector_store.pkl')
        with open(path, 'wb') as f:
            pickle.dump(data, f)
        logger.info(f"Vector store saved to {path}")
    
    def load(self):
        """Load vector store from disk."""
        path = os.path.join(self.storage_path, 'vector_store.pkl')
        if os.path.exists(path):
            with open(path, 'rb') as f:
                data = pickle.load(f)
            self.vectors = data['vectors']
            self.metadata = data['metadata']
            self.dimension = data['dimension']
            logger.info(f"Vector store loaded from {path}. Total vectors: {len(self.vectors)}")
        else:
            logger.info("No existing vector store found")
    
    def clear(self):
        """Clear all vectors."""
        self.vectors = []
        self.metadata = []
        self.dimension = None
        logger.info("Vector store cleared")
