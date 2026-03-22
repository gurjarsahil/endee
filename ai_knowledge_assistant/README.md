# AI Knowledge Assistant - RAG + Vector Database

A production-level AI-powered question-answering system using Retrieval Augmented Generation (RAG) with a vector database inspired by Endee architecture.

## Features

- 📄 **PDF Document Processing** - Upload and process PDF documents
- 🔍 **Semantic Search** - Find relevant information using vector similarity
- 🤖 **AI-Powered Answers** - Generate accurate answers using Google Gemini
- 💾 **Vector Database** - Efficient storage and retrieval using Endee-inspired architecture
- 📊 **Similarity Scores** - View relevance scores for retrieved context
- 🎨 **Clean UI** - User-friendly Streamlit interface
- 📝 **Logging** - Comprehensive logging for debugging

## Architecture

```
┌─────────────┐
│   PDF File  │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Data Loader    │  ← Extracts text and creates chunks
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Embeddings     │  ← Converts text to vectors (sentence-transformers)
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  Vector Store   │  ← Stores vectors with metadata (Endee-inspired)
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│  RAG Pipeline   │  ← Retrieves context + generates answer (Gemini)
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│   Streamlit UI  │  ← Interactive web interface
└─────────────────┘
```

## Project Structure

```
ai_knowledge_assistant/
├── data_loader.py      # PDF loading and text chunking
├── embeddings.py       # Sentence transformer embeddings
├── vector_store.py     # Vector database (Endee-inspired)
├── rag_pipeline.py     # RAG orchestration and LLM integration
├── app.py              # Streamlit web application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Google Gemini API key (get it from https://makersuite.google.com/app/apikey)

### Setup Steps

1. **Clone or navigate to the project directory:**
```bash
cd ai_knowledge_assistant
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Linux/Mac:
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up your Gemini API key:**

You can either:
- Enter it in the web interface sidebar, or
- Set it as an environment variable:

```bash
# Windows:
set GEMINI_API_KEY=your_api_key_here

# Linux/Mac:
export GEMINI_API_KEY=your_api_key_here
```

## Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

### Using the Application

1. **Enter API Key** (in sidebar)
   - Paste your Google Gemini API key

2. **Upload PDF Document**
   - Click "Browse files" in the sidebar
   - Select a PDF file
   - Click "Process PDF"
   - Wait for processing to complete

3. **Ask Questions**
   - Type your question in the main area
   - Adjust the number of context chunks (1-10)
   - Click "Search"
   - View the AI-generated answer and retrieved context

4. **View Context**
   - Expand context sections to see retrieved text chunks
   - Check similarity scores to understand relevance

## Module Details

### data_loader.py
- **PDFLoader**: Extracts text from PDF files
- **chunk_text()**: Splits text into overlapping chunks for better context preservation
- Configurable chunk size and overlap

### embeddings.py
- **EmbeddingModel**: Wraps sentence-transformers
- Uses `all-MiniLM-L6-v2` model (384 dimensions)
- Efficient batch encoding

### vector_store.py
- **VectorStore**: Simulated vector database inspired by Endee
- Cosine similarity search
- Persistent storage using pickle
- Metadata tracking for each vector

### rag_pipeline.py
- **RAGPipeline**: Orchestrates retrieval and generation
- Converts queries to embeddings
- Retrieves top-k similar chunks
- Generates answers using Gemini API
- Returns structured results with context and scores

### app.py
- **Streamlit UI**: Clean, intuitive interface
- Real-time processing feedback
- Database statistics
- Error handling and logging

## Configuration

### Chunk Size and Overlap
Edit in `app.py`:
```python
loader = PDFLoader(chunk_size=500, overlap=50)
```

### Embedding Model
Edit in `embeddings.py`:
```python
self.model = SentenceTransformer('all-MiniLM-L6-v2')
# Other options: 'all-mpnet-base-v2', 'paraphrase-multilingual-MiniLM-L12-v2'
```

### Vector Store Path
Edit in `vector_store.py`:
```python
VectorStore(storage_path="./vector_db")
```

## Logging

Logs are displayed in the console where you run the application. They include:
- PDF processing status
- Embedding generation progress
- Vector store operations
- Search queries and results
- Error messages

## Troubleshooting

### "No module named 'sentence_transformers'"
```bash
pip install sentence-transformers
```

### "API key not found"
Make sure you've entered your Gemini API key in the sidebar or set the environment variable.

### "Vector store is empty"
Upload and process a PDF document first before asking questions.

### Slow first run
The first time you run the app, it downloads the embedding model (~80MB). Subsequent runs are faster.

## Performance Tips

1. **Chunk Size**: Smaller chunks (300-500 words) work better for specific questions
2. **Top-K**: Use 3-5 chunks for balanced context
3. **Batch Processing**: Process multiple PDFs before querying
4. **Model Selection**: Use larger models for better accuracy (at the cost of speed)

## Future Enhancements

- [ ] Support for multiple document formats (DOCX, TXT, HTML)
- [ ] Integration with actual Endee vector database
- [ ] Advanced filtering and metadata search
- [ ] Multi-language support
- [ ] Conversation history
- [ ] Export results to PDF/JSON
- [ ] Hybrid search (dense + sparse vectors)

## License

This project is built as a demonstration of RAG architecture using Endee-inspired vector database design.

## Acknowledgments

- **Endee** - Vector database architecture inspiration
- **Sentence Transformers** - Embedding generation
- **Google Gemini** - LLM for answer generation
- **Streamlit** - Web interface framework

## Contact

For questions or issues, please refer to the Endee documentation at https://docs.endee.io

---

**Built with ❤️ using Endee-inspired architecture**
