# AI Knowledge Assistant - Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE (Streamlit)                   │
│  ┌──────────────────┐              ┌──────────────────────────┐    │
│  │   Sidebar        │              │     Main Area            │    │
│  │  - API Key Input │              │  - Query Input           │    │
│  │  - PDF Upload    │              │  - Search Button         │    │
│  │  - Process Button│              │  - Answer Display        │    │
│  │  - DB Stats      │              │  - Context Display       │    │
│  │  - Clear DB      │              │  - Similarity Scores     │    │
│  └──────────────────┘              └──────────────────────────┘    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      RAG PIPELINE (rag_pipeline.py)                  │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  1. Convert query to embedding                               │  │
│  │  2. Search vector store for similar chunks                   │  │
│  │  3. Retrieve top-k results with scores                       │  │
│  │  4. Build context-aware prompt                               │  │
│  │  5. Generate answer using Gemini API                         │  │
│  │  6. Return structured result                                 │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────┬──────────────────────────────────┬─────────────────────┘
             │                                  │
             ▼                                  ▼
┌────────────────────────────┐    ┌────────────────────────────────┐
│  EMBEDDING MODEL           │    │  VECTOR STORE                  │
│  (embeddings.py)           │    │  (vector_store.py)             │
│                            │    │                                │
│  - Model: all-MiniLM-L6-v2 │    │  - Storage: Numpy arrays       │
│  - Dimension: 384          │    │  - Search: Cosine similarity   │
│  - Batch encoding          │    │  - Persistence: Pickle         │
│  - Single encoding         │    │  - Metadata: ID, text, index   │
└────────────────────────────┘    └────────────────────────────────┘
             ▲                                  ▲
             │                                  │
             └──────────────┬───────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    DATA LOADER (data_loader.py)                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  1. Load PDF file (PyPDF2)                                   │  │
│  │  2. Extract text from all pages                              │  │
│  │  3. Split into chunks (500 words, 50 overlap)                │  │
│  │  4. Return list of text chunks                               │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
                      ┌──────────────┐
                      │  PDF FILES   │
                      └──────────────┘
```

## Data Flow - Document Processing

```
PDF Upload
    │
    ▼
┌─────────────────┐
│  Load PDF       │  ← PyPDF2.PdfReader
│  Extract Text   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Chunk Text     │  ← Split into 500-word chunks with 50-word overlap
│  Create List    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Generate       │  ← Sentence Transformers (all-MiniLM-L6-v2)
│  Embeddings     │  ← Convert each chunk to 384-dim vector
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Store Vectors  │  ← Save to vector_store with metadata
│  + Metadata     │  ← {id, text, chunk_index}
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Persist to     │  ← Pickle to disk (vector_db/vector_store.pkl)
│  Disk           │
└─────────────────┘
```

## Data Flow - Query Processing

```
User Query
    │
    ▼
┌─────────────────┐
│  Convert to     │  ← Sentence Transformers
│  Embedding      │  ← 384-dim vector
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Similarity     │  ← Cosine similarity with all stored vectors
│  Search         │  ← Normalize vectors (L2 norm)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Retrieve       │  ← Get top-k results (default k=3)
│  Top-K Results  │  ← Sort by similarity score
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Build Prompt   │  ← Combine query + context
│  with Context   │  ← Format for LLM
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Generate       │  ← Google Gemini API (gemini-pro)
│  Answer         │  ← Context-aware response
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Return Result  │  ← {query, context[], answer}
│  to UI          │  ← Display with similarity scores
└─────────────────┘
```

## Module Dependencies

```
app.py
  ├── data_loader.py
  │     └── PyPDF2
  ├── embeddings.py
  │     └── sentence-transformers
  │           └── torch
  ├── vector_store.py
  │     ├── numpy
  │     └── pickle
  └── rag_pipeline.py
        ├── embeddings.py
        ├── vector_store.py
        └── google.generativeai
```

## File Structure

```
ai_knowledge_assistant/
│
├── Core Modules
│   ├── data_loader.py      (PDF → Text Chunks)
│   ├── embeddings.py       (Text → Vectors)
│   ├── vector_store.py     (Vector Storage & Search)
│   ├── rag_pipeline.py     (Retrieval + Generation)
│   └── app.py              (Web Interface)
│
├── Configuration
│   ├── config.py           (Settings)
│   └── requirements.txt    (Dependencies)
│
├── Documentation
│   ├── README.md           (Setup Guide)
│   ├── PROJECT_OVERVIEW.md (Technical Docs)
│   ├── QUICK_REFERENCE.md  (Quick Commands)
│   └── PROJECT_COMPLETE.md (Summary)
│
├── Utilities
│   ├── test_setup.py       (Verification)
│   ├── example_usage.py    (Programmatic Example)
│   ├── quick_start.bat     (Windows Setup)
│   └── quick_start.sh      (Linux/Mac Setup)
│
└── Other
    └── .gitignore          (Git Ignore Rules)
```

## Vector Store Architecture (Endee-Inspired)

```
┌─────────────────────────────────────────────────────────────┐
│                    VECTOR STORE                             │
│                                                             │
│  ┌───────────────────────────────────────────────────┐    │
│  │  In-Memory Storage                                │    │
│  │  ┌─────────────────────────────────────────────┐  │    │
│  │  │  vectors: List[np.ndarray]                  │  │    │
│  │  │    - Shape: (n_docs, 384)                   │  │    │
│  │  │    - Type: float32                          │  │    │
│  │  │    - Normalized: L2 norm                    │  │    │
│  │  └─────────────────────────────────────────────┘  │    │
│  │                                                    │    │
│  │  ┌─────────────────────────────────────────────┐  │    │
│  │  │  metadata: List[Dict]                       │  │    │
│  │  │    - id: int                                │  │    │
│  │  │    - text: str                              │  │    │
│  │  │    - chunk_index: int                       │  │    │
│  │  └─────────────────────────────────────────────┘  │    │
│  └───────────────────────────────────────────────────┘    │
│                                                             │
│  ┌───────────────────────────────────────────────────┐    │
│  │  Search Algorithm                                 │    │
│  │  1. Normalize query vector (L2)                  │    │
│  │  2. Normalize all stored vectors (L2)            │    │
│  │  3. Compute dot product (cosine similarity)      │    │
│  │  4. Sort by similarity (descending)              │    │
│  │  5. Return top-k results                         │    │
│  └───────────────────────────────────────────────────┘    │
│                                                             │
│  ┌───────────────────────────────────────────────────┐    │
│  │  Persistence (Pickle)                             │    │
│  │  File: vector_db/vector_store.pkl                │    │
│  │  Contains: {vectors, metadata, dimension}        │    │
│  └───────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                     TECHNOLOGY STACK                        │
├─────────────────────────────────────────────────────────────┤
│  Frontend                                                   │
│    └── Streamlit 1.31.0                                    │
├─────────────────────────────────────────────────────────────┤
│  Embeddings                                                 │
│    ├── Sentence Transformers 2.3.1                         │
│    └── PyTorch 2.1.2                                       │
├─────────────────────────────────────────────────────────────┤
│  Vector Operations                                          │
│    └── NumPy 1.24.3                                        │
├─────────────────────────────────────────────────────────────┤
│  Document Processing                                        │
│    └── PyPDF2 3.0.1                                        │
├─────────────────────────────────────────────────────────────┤
│  LLM Integration                                            │
│    └── Google Generative AI 0.3.2                          │
├─────────────────────────────────────────────────────────────┤
│  Storage                                                    │
│    └── Pickle (Python Standard Library)                    │
├─────────────────────────────────────────────────────────────┤
│  Logging                                                    │
│    └── Python Logging (Standard Library)                   │
└─────────────────────────────────────────────────────────────┘
```

## Performance Metrics

```
┌─────────────────────────────────────────────────────────────┐
│                    PERFORMANCE METRICS                      │
├─────────────────────────────────────────────────────────────┤
│  Operation              │  Time          │  Notes           │
├─────────────────────────┼────────────────┼──────────────────┤
│  PDF Loading            │  1-2s/page     │  Depends on size │
│  Text Chunking          │  <100ms        │  Fast            │
│  Embedding (100 chunks) │  ~1s           │  CPU-based       │
│  Vector Storage         │  <50ms         │  In-memory       │
│  Similarity Search      │  <100ms        │  10k vectors     │
│  LLM Generation         │  2-5s          │  API latency     │
│  Total Query Time       │  3-6s          │  End-to-end      │
├─────────────────────────┴────────────────┴──────────────────┤
│  Memory Usage                                               │
│    - Base: ~200MB (model loaded)                           │
│    - Per 1000 chunks: ~4MB (384-dim vectors)               │
│    - Scalable to: ~100k vectors on 8GB RAM                 │
└─────────────────────────────────────────────────────────────┘
```

---

**Architecture Version**: 1.0.0  
**Last Updated**: 2024  
**Status**: Production-Ready ✅
