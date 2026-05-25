import chromadb
from chromadb.config import Settings
from app.config import settings
from typing import List, Dict, Any

client = chromadb.Client(Settings(
    persist_directory=settings.CHROMA_PATH,
    anonymized_telemetry=False
))

collection = client.get_or_create_collection("ops_knowledge")

def add_document(doc_id: str, content: str, metadata: Dict[str, Any] = None):
    if metadata is None:
        metadata = {}
    
    collection.add(
        documents=[content],
        metadatas=[metadata],
        ids=[doc_id]
    )
    client.persist()

def search_similar(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    results_list = []
    for i in range(len(results['ids'][0])):
        results_list.append({
            'id': results['ids'][0][i],
            'title': results['metadatas'][0][i].get('title', ''),
            'content': results['documents'][0][i],
            'similarity': results['distances'][0][i] if results['distances'] else 0.7
        })
    
    return results_list

def get_all_docs() -> List[Dict[str, Any]]:
    results = collection.get()
    docs = []
    for i, doc_id in enumerate(results['ids']):
        docs.append({
            'id': doc_id,
            'title': results['metadatas'][i].get('title', ''),
            'content': results['documents'][i]
        })
    return docs

def delete_document(doc_id: str):
    collection.delete(ids=[doc_id])
    client.persist()

def count_documents() -> int:
    return collection.count()
