from sentence_transformers import SentenceTransformer
import numpy as np
import logging
from typing import List

logger = logging.getLogger(__name__)

class EmbeddingModel:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        logger.info(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        logger.info(f"Model loaded. Embedding dimension: {self.dimension}")
    
    def encode(self, texts: List[str]) -> np.ndarray:
        """Convert texts to embeddings."""
        embeddings = self.model.encode(texts, show_progress_bar=True)
        logger.info(f"Encoded {len(texts)} texts")
        return embeddings
    
    def encode_single(self, text: str) -> np.ndarray:
        """Convert single text to embedding."""
        return self.model.encode([text])[0]
