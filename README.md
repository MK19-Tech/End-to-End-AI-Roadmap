# 🤖 Agentic-RAG: Private Local Intelligence System

An end-to-end, privacy-focused **Agentic Retrieval-Augmented Generation (RAG)** system. This application allows you to chat with your local documents while empowering a **Llama 3.1** agent to autonomously search the web when local data isn't enough.

---

## 🏗️ Repository Structure
```text
├── data/                   # Input PDFs/Text files
├── utils/                  # Core logic
│   ├── loaders.py          # PDF/Text extraction
│   ├── processors.py       # Text cleaning & Sentiment Analysis
│   ├── chunkers.py         # Text splitting
│   ├── savers.py           # JSON exports
│   ├── retriever.py        # Vector search logic
│   └── vector_store.py     # ChromaDB management
├── chroma_db/              # Local Vector Database (ignored by git)
├── main.py                 # Document Ingestion Script
├── agentic_search.py       # LangGraph Agent logic
├── app.py                  # Streamlit UI
├── config.yaml.example     # Template for user/friend access
├── Dockerfile              # Containerization instructions
├── requirements.txt        # Updated dependency list
└── README.md               # Professional documentation
```

---

## 🌟 Key Features
- **Autonomous Routing**: Uses **LangGraph** to decide between local PDFs or live web search.
- **Sentiment Insight**: Integrated **Hugging Face Transformers** (via `distilbert-base-uncased`) to analyze the sentiment of retrieved context.
- **100% Local**: Powered by **Ollama (Llama 3.1)**; your data never leaves your machine.
- **Web-Augmented**: Uses **Tavily Search API** to fill gaps when local docs don't have the answer.

---

## 💻 System Requirements
Running **Llama 3.1 (8B)** locally is hardware-intensive:
- **RAM**: 8GB Minimum (16GB Recommended).
- **GPU**: NVIDIA RTX 3060+ (8GB VRAM) for optimal speed.
- **Disk**: ~10GB total (Model + Dependencies).
- **CPU**: Works on CPU-only machines but will be slower (30-60s per response).

---

## 🚀 Getting Started
### 1. Prerequisites
- **Ollama**: Download and install from [ollama.com](https://ollama.com).
- **Model**: Run `ollama pull llama3.1` in your terminal.

### 2. Configuration
Create a `.env` file in the root directory:
```env
OLLAMA_BASE_URL=http://localhost:11434

---

## 🐳 Docker Deployment
```bash
docker build -t agentic-rag .
docker run -p 8501:8501 agentic-rag
```
