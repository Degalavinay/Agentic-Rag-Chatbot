from typing import List
from utils.mcp import MCPMessage, MessageType
from utils.document_parser import DocumentParser

class IngestionAgent:
    def __init__(self):
        self.chunk_size = 1000
        self.chunk_overlap = 200

    def _chunk_text(self, text: str) -> List[str]:
        """Split text into chunks with overlap"""
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunks.append(text[start:end])
            start = end - self.chunk_overlap
        
        return chunks

    def process(self, message: MCPMessage) -> MCPMessage:
        """Process document upload message"""
        if message.message_type != MessageType.DOCUMENT_UPLOAD:
            raise ValueError("Invalid message type for IngestionAgent")

        chunks = []
        for file_path in message.payload["file_paths"]:
            try:
                content = DocumentParser.parse(file_path)
                for chunk in self._chunk_text(content):
                    chunks.append({
                        "content": chunk,
                        "source": file_path
                    })
            except Exception as e:
                return MCPMessage(
                    sender="IngestionAgent",
                    receiver=message.sender,
                    message_type=MessageType.ERROR,
                    payload={"error": str(e)},
                    trace_id=message.trace_id
                )

        return MCPMessage(
            sender="IngestionAgent",
            receiver="RetrievalAgent",
            message_type=MessageType.DOCUMENTS_INGESTED,
            payload={"documents": chunks},
            trace_id=message.trace_id
        )
