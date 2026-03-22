import os
import logging
from typing import List, Dict, Optional
import google.generativeai as genai

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self, vector_store, embedding_model, api_key: Optional[str] = None):
        self.vector_store = vector_store
        self.embedding_model = embedding_model
        
        # Configure Gemini API
        api_key = api_key or os.getenv('GEMINI_API_KEY')
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            logger.info("Gemini API configured")
        else:
            self.model = None
            logger.warning("No API key provided. LLM generation disabled")
    
    def query(self, question: str, top_k: int = 3) -> Dict:
        """Execute RAG pipeline: retrieve context and generate answer."""
        logger.info(f"Processing query: {question}")
        
        # Step 1: Convert query to embedding
        query_embedding = self.embedding_model.encode_single(question)
        
        # Step 2: Retrieve similar chunks
        results = self.vector_store.search(query_embedding, top_k=top_k)
        
        if not results:
            return {
                'query': question,
                'context': [],
                'answer': 'No relevant information found in the knowledge base.',
                'error': 'Empty vector store'
            }
        
        # Step 3: Prepare context
        context_items = []
        for doc_id, score, text in results:
            context_items.append({
                'id': doc_id,
                'score': round(score, 4),
                'text': text[:500]  # Truncate for display
            })
        
        context_text = "\n\n".join([item['text'] for item in context_items])
        
        # Step 4: Generate answer using LLM
        if self.model:
            try:
                prompt = self._build_prompt(question, context_text)
                response = self.model.generate_content(prompt)
                answer = response.text
                logger.info("Answer generated successfully")
            except Exception as e:
                logger.error(f"Error generating answer: {e}")
                answer = f"Error generating answer: {str(e)}"
        else:
            answer = "LLM not configured. Please set GEMINI_API_KEY environment variable."
        
        return {
            'query': question,
            'context': context_items,
            'answer': answer
        }
    
    def _build_prompt(self, question: str, context: str) -> str:
        """Build prompt for LLM."""
        return f"""You are a helpful AI assistant. Answer the question based on the provided context.

Context:
{context}

Question: {question}

Answer: Provide a clear, concise answer based only on the context above. If the context doesn't contain enough information, say so."""
