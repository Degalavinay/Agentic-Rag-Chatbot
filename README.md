## Agentic RAG Chatbot
A modular, agent-based Retrieval-Augmented Generation (RAG) chatbot for question-answering over multiple document formats (PDF, DOCX, CSV, PPTX, TXT, MD). Built with Streamlit, FAISS, Sentence Transformers, and a lightweight LLM (GPT-2, with optional OpenAI support).

## Features
Multi-Format Document Support: Upload and process PDF, DOCX, CSV, PPTX, TXT, and MD files.
Semantic Search: Uses FAISS and all-MiniLM-L6-v2 for efficient document retrieval.
Agent-Based Architecture: Modular design with ingestion, retrieval, and response generation agents.
Interactive UI: Streamlit-based interface with drag-and-drop file uploads and query input.
Source Attribution: Displays answers with references to source documents.
Extensible LLM: Supports GPT-2 by default, with easy integration for other models (e.g., OpenAI via .env).

## Directory Structure
rag_chatbot/
├── agents/
│   ├── ingestion_agent.py      # Handles document parsing and chunking
│   ├── retrieval_agent.py      # Manages vector storage and search
│   ├── llm_response_agent.py   # Generates answers using LLM
│   └── coordinator_agent.py    # Orchestrates agent workflows
├── utils/
│   ├── mcp.py                 # Model Context Protocol for agent communication
│   ├── document_parser.py     # Parses various document formats
│   └── vector_store.py        # FAISS-based vector storage and search
├── ui/
│   └── app.py                 # Streamlit UI for file uploads and queries
├── data/
│   ├── uploads/               # Stores uploaded documents
│   └── vector_store/          # Placeholder for persistent vector storage
├── run.bat                    # Windows script to launch Streamlit
├── requirements.txt           # Python dependencies
├── __init__.py                # Marks project as a Python package
└── README.md                  # This file

## Requirements
Python 3.8+
Dependencies (listed in requirements.txt):
streamlit==1.24.0
PyPDF2==3.0.1
python-docx==0.8.11
python-pptx==0.6.23
pandas==2.0.3
sentence-transformers==2.2.2
faiss-cpu==1.7.2
transformers==4.37.0
torch==2.1.0
Setup

## Clone the Repository:
git clone <repository-url>
cd rag_chatbot

## Install Dependencies:
pip install -r requirements.txt

## Create Data Directories:
mkdir -p data/uploads data/vector_store

## Optional: Configure OpenAI API (for advanced LLM support):
echo OPENAI_API_KEY=your-key > .env

## Launch the Application:
## On Windows:
run.bat

## Or directly:
streamlit run ui/app.py

## Usage
## Upload Documents:
Open the Streamlit UI (default: http://localhost:8501).
In the sidebar, upload files (PDF, DOCX, CSV, PPTX, TXT, MD) using the file uploader.
Click "Process" to ingest documents.
Ask Questions:
Enter a question in the main panel's text input (e.g., "What were the Q1 revenue figures?").
Click "Submit" to get an answer with source references.
Example Output:
Input: Upload q1_report.pdf and ask, "What were the Q1 revenue figures?"

## Output:
Answer:
- Revenue: $1.5M (+20% QoQ)
- New Customers: 150
Sources:
1. data/uploads/q1_report.pdf
   Revenue for Q1 was reported at $1.5 million, a 20% increase quarter-over-quarter...

## Architecture
The system uses an agent-based RAG architecture with the following components:
## Model Context Protocol (MCP) (mcp.py):
JSON-based message-passing system with sender, receiver, message_type, payload, and trace_id.
Supports message types: DOCUMENT_UPLOAD, DOCUMENTS_INGESTED, QUERY_REQUEST, RETRIEVAL_RESULT, RESPONSE_READY, ERROR.
## Ingestion Agent (ingestion_agent.py):
Parses documents using DocumentParser.
Chunks text (1000 characters, 200 overlap) and adds metadata (source, content).
## Retrieval Agent (retrieval_agent.py):
Stores document embeddings in a FAISS index using all-MiniLM-L6-v2.
Performs semantic search to retrieve top-k (default k=3) relevant documents.
## LLM Response Agent (llm_response_agent.py):
Generates answers using GPT-2 (or OpenAI if configured).
Constructs prompts with context and query; cleans responses to remove duplicates.
## Coordinator Agent (coordinator_agent.py):
Orchestrates document upload and query processing workflows.
Tracks system readiness to ensure documents are processed before queries.

## Streamlit UI (app.py):
Provides a web interface for file uploads and queries.
Displays answers and source snippets (up to 200 characters).

## Technical Details
Embedding Model: all-MiniLM-L6-v2 (Sentence Transformers) for document and query embeddings.
Vector Store: FAISS with FlatL2 index for similarity search.
LLM: GPT-2 by default; supports OpenAI via .env configuration.
Chunking: 1000-character chunks with 200-character overlap.
UI: Streamlit with drag-and-drop file upload and query input.

## Known Limitations
No Chat History: The UI lacks session state for multi-turn conversations.
Non-Persistent Index: FAISS index is rebuilt on each run, ignoring data/vector_store/.
Basic Error Handling: Limited feedback for file parsing errors or agent failures.
CPU-Only FAISS: No GPU acceleration, limiting scalability.
Source Truncation: Source content is capped at 200 characters in the UI.
Lightweight LLM: GPT-2 may produce suboptimal answers compared to larger models.

## Future Improvements
UI Enhancements:
Add chat history using st.session_state.
Display full source content or expandable snippets.
Show progress bars for uploads and queries.
Add document management (list, delete, view metadata).

## Persistence:
Save FAISS index to data/vector_store/ for reuse.
Store document metadata in a database (e.g., SQLite).

## Functionality:
Implement hybrid search (keyword + semantic).
Support multi-turn conversations with context.
Use dynamic chunking (e.g., sentence-aware splitting).

## Performance:
Upgrade to faiss-gpu for faster indexing/search.
Replace GPT-2 with a more powerful LLM (e.g., LLaMA).
Cache frequent queries for faster responses.

## Robustness:
Enhance error handling with detailed feedback.
Add logging for debugging and monitoring.
Implement retry logic for agent failures.

## Testing:
Add a tests/ directory with unit and integration tests.
Test edge cases (corrupt files, empty queries, large documents).
Contributing
Contributions are welcome! Please:

## Fork the repository.
Create a feature branch (git checkout -b feature-name).
Commit changes (git commit -m "Add feature").
Push to the branch (git push origin feature-name).
Open a pull request.
