from utils.mcp import MCPMessage, MessageType
from typing import Dict, Any

class CoordinatorAgent:
    def __init__(self, ingestion_agent, retrieval_agent, response_agent):
        self.ingestion_agent = ingestion_agent
        self.retrieval_agent = retrieval_agent
        self.response_agent = response_agent
        self.ready = False

    def process_upload(self, file_paths: list[str]) -> Dict[str, Any]:
        """Coordinate document upload process"""
        message = MCPMessage(
            sender="Coordinator",
            receiver="IngestionAgent",
            message_type=MessageType.DOCUMENT_UPLOAD,
            payload={"file_paths": file_paths}
        )
        
        ingestion_response = self.ingestion_agent.process(message)
        retrieval_response = self.retrieval_agent.process(ingestion_response)
        
        if retrieval_response.message_type == MessageType.RESPONSE_READY:
            self.ready = True
            return {"status": "success"}
        else:
            return {"status": "error", "message": "Processing failed"}

    def process_query(self, query: str) -> Dict[str, Any]:
        """Coordinate query processing"""
        if not self.ready:
            return {"error": "Documents not processed yet"}
        
        message = MCPMessage(
            sender="Coordinator",
            receiver="RetrievalAgent",
            message_type=MessageType.QUERY_REQUEST,
            payload={"query": query}
        )
        
        retrieval_response = self.retrieval_agent.process(message)
        final_response = self.response_agent.process(retrieval_response)
        
        return final_response.payload
