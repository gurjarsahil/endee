# Quick Reference Guide

## 🚀 Quick Start Commands

### Windows
```bash
# Setup
quick_start.bat

# Run application
venv\Scripts\activate
streamlit run app.py
```

### Linux/Mac
```bash
# Setup
chmod +x quick_start.sh
./quick_start.sh

# Run application
source venv/bin/activate
streamlit run app.py
```

## 📝 Common Tasks

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Test Setup
```bash
python test_setup.py
```

### 3. Run Application
```bash
streamlit run app.py
```

### 4. Programmatic Usage
```bash
python example_usage.py
```

## 🔑 API Key Setup

### Option 1: Environment Variable (Recommended)
```bash
# Windows
set GEMINI_API_KEY=your_api_key_here

# Linux/Mac
export GEMINI_API_KEY=your_api_key_here
```

### Option 2: In Application
Enter your API key in the sidebar when the app is running.

## 📂 File Structure

```
ai_knowledge_assistant/
├── app.py                  # Main Streamlit application
├── data_loader.py          # PDF loading and chunking
├── embeddings.py           # Embedding generation
├── vector_store.py         # Vector database
├── rag_pipeline.py         # RAG orchestration
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── test_setup.py          # Setup verification
├── example_usage.py       # Programmatic example
├── README.md              # Main documentation
├── PROJECT_OVERVIEW.md    # Technical overview
└── quick_start.bat/sh     # Setup scripts
```

## 🎯 Usage Workflow

1. **Start Application**
   ```bash
   streamlit run app.py
   ```

2. **Enter API Key** (in sidebar)

3. **Upload PDF**
   - Click "Browse files"
   - Select PDF
   - Click "Process PDF"

4. **Ask Questions**
   - Type question in main area
   - Adjust top-k slider (1-10)
   - Click "Search"

5. **View Results**
   - Read AI-generated answer
   - Expand context sections
   - Check similarity scores

## ⚙️ Configuration

### Change Embedding Model
Edit `config.py`:
```python
EMBEDDING_MODEL = 'all-mpnet-base-v2'  # Better quality
```

### Adjust Chunk Size
Edit `config.py`:
```python
CHUNK_SIZE = 300      # Smaller chunks
CHUNK_OVERLAP = 30    # Less overlap
```

### Change Storage Path
Edit `config.py`:
```python
VECTOR_STORE_PATH = './my_custom_db'
```

## 🐛 Troubleshooting

### Import Errors
```bash
pip install --upgrade -r requirements.txt
```

### Model Download Issues
```bash
# Clear cache and retry
rm -rf ~/.cache/torch/sentence_transformers/
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

### API Key Errors
- Verify key is correct
- Check internet connection
- Ensure key has Gemini API access

### Empty Results
- Ensure PDF is processed first
- Check database stats in sidebar
- Try different questions

## 📊 Performance Tips

### For Large PDFs
```python
# Use smaller chunks
CHUNK_SIZE = 300
CHUNK_OVERLAP = 30
```

### For Better Accuracy
```python
# Use larger model
EMBEDDING_MODEL = 'all-mpnet-base-v2'

# Retrieve more context
top_k = 5
```

### For Faster Processing
```python
# Use default model
EMBEDDING_MODEL = 'all-MiniLM-L6-v2'

# Fewer results
top_k = 3
```

## 🔍 Debugging

### Enable Debug Logging
Edit `config.py`:
```python
LOG_LEVEL = "DEBUG"
```

### Check Vector Store
```python
from vector_store import VectorStore
store = VectorStore()
store.load()
print(f"Total vectors: {len(store.vectors)}")
```

### Test Embeddings
```python
from embeddings import EmbeddingModel
model = EmbeddingModel()
emb = model.encode_single("test")
print(f"Embedding shape: {emb.shape}")
```

## 📦 Backup & Restore

### Backup Database
```bash
# Copy vector_db folder
cp -r vector_db vector_db_backup
```

### Restore Database
```bash
# Replace with backup
rm -rf vector_db
cp -r vector_db_backup vector_db
```

### Clear Database
In the application sidebar, click "Clear Database"

## 🌐 Deployment

### Local Network Access
```bash
streamlit run app.py --server.address 0.0.0.0
```

### Custom Port
```bash
streamlit run app.py --server.port 8501
```

### Production Deployment
Consider using:
- Docker container
- Cloud platforms (AWS, GCP, Azure)
- Streamlit Cloud

## 📞 Support

- Check README.md for detailed documentation
- Review PROJECT_OVERVIEW.md for technical details
- Run test_setup.py to verify installation
- Check logs for error messages

## 🔗 Useful Links

- [Streamlit Docs](https://docs.streamlit.io)
- [Sentence Transformers](https://www.sbert.net/)
- [Gemini API](https://ai.google.dev/)
- [Endee Docs](https://docs.endee.io)

---

**Quick Help**: Run `python test_setup.py` to verify your setup
