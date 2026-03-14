git statusimport chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict
import os

class VectorDatabase:
    def __init__(self, collection_name: str = "resume_collection", persist_directory: str = "./chroma_db"):
        print("Loading embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.Client(Settings(persist_directory=persist_directory, anonymized_telemetry=False))
        try:
            self.collection = self.client.get_collection(name=collection_name)
            print(f"Loaded existing collection '{collection_name}'")
        except:
            self.collection = self.client.create_collection(name=collection_name, metadata={"description": "Resume and projects knowledge base"})
            print(f"Created new collection '{collection_name}'")
    
    def add_documents(self, documents: List[Dict[str, str]]):
        print(f"Adding {len(documents)} document chunks to vector database...")
        ids = []
        embeddings = []
        metadatas = []
        documents_text = []
        for i, doc in enumerate(documents):
            embedding = self.embedding_model.encode(doc['content']).tolist()
            ids.append(f"doc_{i}")
            embeddings.append(embedding)
            metadatas.append({'filename': doc.get('filename', 'unknown'), 'source': doc.get('source', 'unknown')})
            documents_text.append(doc['content'])
        self.collection.add(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents_text)
        print(f"Successfully added {len(documents)} chunks to database!")
    
    def search(self, query: str, n_results: int = 3) -> List[Dict]:
        query_embedding = self.embedding_model.encode(query).tolist()
        results = self.collection.query(query_embeddings=[query_embedding], n_results=n_results)
        formatted_results = []
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({'content': doc, 'metadata': results['metadatas'][0][i] if results['metadatas'] else {}, 'distance': results['distances'][0][i] if results.get('distances') else 0})
        return formatted_results
    
    def get_collection_count(self) -> int:
        return self.collection.count()
    
    def reset_collection(self):
        collection_name = self.collection.name
        self.client.delete_collection(name=collection_name)
        self.collection = self.client.create_collection(name=collection_name, metadata={"description": "Resume and projects knowledge base"})
        print(f"Collection '{collection_name}' reset successfully!")
