import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class VectorStore:
    def __init__(self):
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.documents = []

    def add_documents(self, documents: List[Dict]):
        """Add documents to the vector store"""
        if not documents:
            return

        embeddings = self.embedder.encode([doc['content'] for doc in documents])
        
        if self.index is None:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])
        
        self.index.add(embeddings)
        self.documents.extend(documents)

    def search(self, query: str, k: int = 3) -> List[Dict]:
        """Search for similar documents"""
        if self.index is None or not self.documents:
            return []

        query_embedding = self.embedder.encode([query])
        distances, indices = self.index.search(query_embedding, k)
        
        return [{
            'document': self.documents[i],
            'score': float(distances[0][j])
        } for j, i in enumerate(indices[0])]
