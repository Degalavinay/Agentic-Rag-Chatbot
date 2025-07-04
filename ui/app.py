import streamlit as st
from agents.coordinator_agent import CoordinatorAgent
from agents.ingestion_agent import IngestionAgent
from agents.retrieval_agent import RetrievalAgent
from agents.llm_response_agent import LLMResponseAgent
import os

def initialize_agents():
    """Initialize all agents"""
    return CoordinatorAgent(
        ingestion_agent=IngestionAgent(),
        retrieval_agent=RetrievalAgent(),
        response_agent=LLMResponseAgent()
    )

def main():
    st.title("Agentic RAG Chatbot")
    
    # Initialize agents
    if 'coordinator' not in st.session_state:
        st.session_state.coordinator = initialize_agents()
    
    # File upload section
    st.sidebar.header("Upload Documents")
    uploaded_files = st.sidebar.file_uploader(
        "Choose files",
        type=["pdf", "pptx", "csv", "docx", "txt", "md"],
        accept_multiple_files=True
    )
    
    if uploaded_files and st.sidebar.button("Process"):
        os.makedirs("data/uploads", exist_ok=True)
        file_paths = []
        
        for file in uploaded_files:
            file_path = f"data/uploads/{file.name}"
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
            file_paths.append(file_path)
        
        result = st.session_state.coordinator.process_upload(file_paths)
        if result["status"] == "success":
            st.sidebar.success("Documents processed successfully!")
        else:
            st.sidebar.error("Error processing documents")
    
    # Chat interface
    st.header("Ask Questions")
    query = st.text_input("Enter your question:")
    
    if st.button("Submit") and query:
        if not uploaded_files:
            st.warning("Please upload documents first")
            return
            
        response = st.session_state.coordinator.process_query(query)
        
        if "error" in response:
            st.error(response["error"])
        else:
            st.subheader("Answer")
            st.write(response["answer"])
            
            st.subheader("Sources")
            for i, source in enumerate(response["sources"][:3], 1):
                st.write(f"{i}. **{source['source']}**")
                st.caption(source['content'][:200] + "...")

if __name__ == "__main__":
    main()
