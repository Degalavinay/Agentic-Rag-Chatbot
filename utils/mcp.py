from dataclasses import dataclass
from enum import Enum
import uuid
from typing import Dict, Any

class MessageType(str, Enum):
    DOCUMENT_UPLOAD = "DOCUMENT_UPLOAD"
    DOCUMENTS_INGESTED = "DOCUMENTS_INGESTED"
    QUERY_REQUEST = "QUERY_REQUEST"
    RETRIEVAL_RESULT = "RETRIEVAL_RESULT"
    RESPONSE_READY = "RESPONSE_READY"
    ERROR = "ERROR"

@dataclass
class MCPMessage:
    sender: str
    receiver: str
    message_type: MessageType
    payload: Dict[str, Any]
    trace_id: str = None

    def __post_init__(self):
        if not self.trace_id:
            self.trace_id = str(uuid.uuid4())
