from fastapi import APIRouter, Depends
from models import KnowledgeSearchRequest, KnowledgeSearchResponse, KnowledgeAskRequest, KnowledgeAskResponse
from rag_service import generate_all_embeddings
from rag_service import answer_with_knowledge
from rag_service import search_similar_documents
from models_db import UsuarioDB
from dependencies import get_current_user

router = APIRouter()

@router.post("/knowledge/search", response_model=KnowledgeSearchResponse)
def knowledge_search(data: KnowledgeSearchRequest, usuario_actual: UsuarioDB = Depends(get_current_user)):
    generate_all_embeddings()
    results = search_similar_documents(data.query, data.top_k)
    return {"results": results}

@router.post("/knowledge/ask", response_model=KnowledgeAskResponse)
def knowledge_ask(data: KnowledgeAskRequest, usuario_actual: UsuarioDB = Depends(get_current_user)):
    generate_all_embeddings()
    result = answer_with_knowledge(data.question, top_k=data.top_k, username=usuario_actual.username)
    return result