Agentic-RAG: Private Local Intelligence System

An end-to-end, privacy-focused Agentic Retrieval-Augmented Generation (RAG) system. This application allows you to chat with your local documents while empowering a Llama 3.1 agent to autonomously search the web when local data isn't enough.

Key Features:

1. Autonomous Routing: Uses LangGraph to decide whether to answer from local PDFs or query the live web.
2. 100% Local & Private: Powered by Ollama (Llama 3.1); your data never leaves your machine.
3. Smart Citations: Automatically labels responses with "📍 Source: Local Docs" or "📍 Source: Web Search."
4. Multi-Tool Integration: Combines ChromaDB (Vector Search) with DuckDuckGo (Web Search).
5. Pro UI: Includes chat history management, session reset, and research export (.txt).

Technical Architecture:

1. Ingestion: main.py chunks and embeds PDFs into a ChromaDB vector store using sentence-transformers.
2. Brain: Llama 3.1 acts as the reasoning engine.
3. Orchestration: A stateful graph manages the "Think -> Act -> Observe" loop.
4. Interface: A clean Streamlit dashboard for user interaction.

Getting Started:

1. Install Ollama; Download the model: ollama pull llama3.1
2. Installation; Clone this repo and install dependencies: git clone https://github.com
                                                           cd agentic-rag-system
                                                           pip install -r requirements.txt

3. a. Usage; Process your documents: Place your PDFs in the /data folder and run: python main.py
   b. Launch the Agent; by running: python -m streamlit run app.py

Project Structure:
├── data/               # Place your PDFs here
├── utils/              # Core logic (loaders, processors, retriever)
├── chroma_db/          # Persistent vector database
├── main.py             # Document ingestion script
├── agentic_search.py   # LangGraph agent logic
└── app.py              # Streamlit UI

Security:
This project includes a Multi-User Authentication layer. Configure your config.yaml to manage user access and secure your private research data.
