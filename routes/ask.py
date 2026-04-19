from fastapi import APIRouter, Depends
from models import AskRequest, AskResponse
from models_db import UsuarioDB
from dependencies import get_current_user
from ai_service import ask_model

router = APIRouter()

@router.post("/ask", response_model=AskResponse)
def ask_question(data: AskRequest, usuario_actual: UsuarioDB = Depends(get_current_user)):
    answer = ask_model(data.question, username=usuario_actual.username)
    return {"answer": answer}