# Agentic RAG Chatbot Implementation

A multi-format document QA system with agent-based Retrieval-Augmented Generation (RAG) architecture using FAISS, TinyLlama (or OpenAI), and Streamlit.

---

## Core Implementation

### Agentic Architecture
- `IngestionAgent`: Parses and chunks PDF, DOCX, PPTX, CSV, TXT
- `RetrievalAgent`: Performs vector search using FAISS and Sentence Transformers
- `LLMResponseAgent`: Generates answers using a chosen LLM (TinyLlama or GPT-3.5)

### Model Context Protocol (MCP)
- JSON-based message passing between agents
- Includes `sender`, `receiver`, `type`, `trace_id`, and `payload`

### Technical Stack
- Python 3.8+
- `sentence-transformers==2.2.2`
- `faiss-cpu`
- `PyPDF2`, `python-docx`, `python-pptx`, `pandas`
- `Streamlit` UI
- Optionally integrates `OpenAI` via `.env` key

---

## Directory Structure

```bash
rag_chatbot/
├── agents/
│   ├── ingestion_agent.py
│   ├── retrieval_agent.py
│   ├── llm_response_agent.py
│   └── coordinator_agent.py
├── utils/
│   ├── mcp.py
│   ├── document_parser.py
│   └── vector_store.py
├── ui/
│   └── app.py
├── data/
│   ├── uploads/
│   └── vector_store/
├── run.bat
├── requirements.txt
└── README.md
```

---

## How to Run

### Step 1: Install Dependencies

```
pip install -r requirements.txt
```

### Step 2: Prepare Environment

```
mkdir data/uploads data/vector_store

# Optional for OpenAI support
echo OPENAI_API_KEY=your-key > .env
```

### Step 3: Launch UI

```
# Windows
run.bat
# Or directly
streamlit run ui/app.py
```

---

## Example Usage

Upload a file like `q1_report.pdf`, and ask:

```text
"What were the Q1 revenue figures?"
```

The system returns:

```text
Answer:
- Revenue: $1.5M (+20% QoQ)
- New Customers: 150
Sources: Page 2 of q1_report.pdf
```

---

## Notes

- Embeddings model: `all-MiniLM-L6-v2`
- Chunk size: 1000 tokens, 200 overlap
- FAISS index is rebuilt on each run
- Streamlit interface supports drag-and-drop

---

## Known Limitations

- CPU-only FAISS (no GPU acceleration)
- No conversation memory or session state
- Limited error handling for corrupt/missing files

---

## Future Improvements

- Add hybrid search (keyword + semantic)
- Support audio/image documents (OCR, ASR)
- Use persistent FAISS index with update ops
- Improve UI with chat history and document highlights

---

