from fastapi import APIRouter, Depends
from models import CopilotRequest, CopilotResponse
from models_db import UsuarioDB
from dependencies import get_current_user
from ai_service import run_copilot

router = APIRouter()

@router.post("/copilot", response_model=CopilotResponse)
def copilot(
    data: CopilotRequest,
    usuario_actual: UsuarioDB = Depends(get_current_user)
):
    return run_copilot(data.text, username=usuario_actual.username)