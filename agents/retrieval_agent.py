from utils.mcp import MCPMessage, MessageType
from utils.vector_store import VectorStore

class RetrievalAgent:
    def __init__(self):
        self.vector_store = VectorStore()

    def process(self, message: MCPMessage) -> MCPMessage:
        """Process incoming messages"""
        if message.message_type == MessageType.DOCUMENTS_INGESTED:
            # Store documents in vector store
            self.vector_store.add_documents(message.payload["documents"])
            return MCPMessage(
                sender="RetrievalAgent",
                receiver="Coordinator",
                message_type=MessageType.RESPONSE_READY,
                payload={"status": "success"},
                trace_id=message.trace_id
            )
        
        elif message.message_type == MessageType.QUERY_REQUEST:
            # Handle query and retrieve relevant documents
            results = self.vector_store.search(message.payload["query"])
            return MCPMessage(
                sender="RetrievalAgent",
                receiver="LLMResponseAgent",
                message_type=MessageType.RETRIEVAL_RESULT,
                payload={
                    "query": message.payload["query"],
                    "context": [res['document'] for res in results],
                    "scores": [res['score'] for res in results]
                },
                trace_id=message.trace_id
            )
        
        else:
            raise ValueError(f"Unsupported message type: {message.message_type}")
