from utils.mcp import MCPMessage, MessageType
from transformers import pipeline
import torch

class LLMResponseAgent:
    def __init__(self):
        self.llm = pipeline(
            "text-generation",
            model="gpt2",
            device="cuda" if torch.cuda.is_available() else "cpu"
        )

    def process(self, message: MCPMessage) -> MCPMessage:
        """Generate response using LLM"""
        if message.message_type != MessageType.RETRIEVAL_RESULT:
            raise ValueError("Invalid message type for LLMResponseAgent")

        context = "\n\n".join(
            f"Source: {doc['source']}\nContent: {doc['content']}" 
            for doc in message.payload["context"]
        )

        prompt = f"""Answer the question based on the context below:

{context}

Question: {message.payload['query']}
Answer:"""

        response = self.llm(
            prompt,
            max_length=200,
            temperature=0.7,
            do_sample=True
        )

        # Clean up the response to avoid redundancy
        answer = response[0]["generated_text"].strip()
        answer = self._clean_response(answer)

        return MCPMessage(
            sender="LLMResponseAgent",
            receiver="UI",
            message_type=MessageType.RESPONSE_READY,
            payload={
                "query": message.payload["query"],
                "answer": answer,
                "sources": message.payload["context"]
            },
            trace_id=message.trace_id
        )

    def _clean_response(self, response: str) -> str:
        """Remove redundant information and format the response"""
        # Example cleaning logic (customize as needed)
        response_lines = response.splitlines()
        unique_lines = list(dict.fromkeys(response_lines))  # Remove duplicates
        return "\n".join(unique_lines)
