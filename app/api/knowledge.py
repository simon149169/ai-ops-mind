from fastapi import APIRouter, HTTPException, File, UploadFile
from app.services.rag_engine import add_document, search_similar, get_all_docs, delete_document, count_documents
from typing import List, Dict, Any
import uuid
import json

router = APIRouter()

@router.post("/upload")
async def upload_knowledge(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="文件名不能为空")
    
    content = await file.read()
    content_str = content.decode('utf-8')
    
    doc_id = str(uuid.uuid4())
    metadata = {'title': file.filename, 'source': 'upload'}
    
    add_document(doc_id, content_str, metadata)
    
    return {'status': 'success', 'doc_id': doc_id, 'title': file.filename}

@router.get("/search")
async def search_knowledge(query: str, top_k: int = 3):
    if not query:
        raise HTTPException(status_code=400, detail="查询关键词不能为空")
    
    results = search_similar(query, top_k)
    return {'results': results}

@router.get("/list")
async def list_knowledge():
    docs = get_all_docs()
    return {'documents': docs, 'count': count_documents()}

@router.delete("/{doc_id}")
async def remove_knowledge(doc_id: str):
    delete_document(doc_id)
    return {'status': 'success', 'message': '文档已删除'}
