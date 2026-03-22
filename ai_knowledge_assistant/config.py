"""
Configuration file for AI Knowledge Assistant
Modify these settings to customize the application behavior
"""

# Embedding Model Configuration
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'  # Options: 'all-mpnet-base-v2', 'paraphrase-multilingual-MiniLM-L12-v2'

# Text Chunking Configuration
CHUNK_SIZE = 500  # Number of words per chunk
CHUNK_OVERLAP = 50  # Number of overlapping words between chunks

# Vector Store Configuration
VECTOR_STORE_PATH = './vector_db'  # Path to store vector database

# Search Configuration
DEFAULT_TOP_K = 3  # Default number of results to retrieve
MAX_TOP_K = 10  # Maximum number of results allowed

# LLM Configuration
LLM_MODEL = 'gemini-pro'  # Gemini model to use
MAX_CONTEXT_LENGTH = 2000  # Maximum characters of context to send to LLM

# UI Configuration
PAGE_TITLE = "AI Knowledge Assistant"
PAGE_ICON = "🤖"

# Logging Configuration
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
