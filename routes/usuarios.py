from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from database import SessionLocal
from models import UsuarioCreate, UsuarioResponse, UsuarioLogin, Token
from models_db import UsuarioDB
from auth import hash_password, verify_password, create_access_token
from dependencies import get_current_user

router = APIRouter()

@router.post("/register", response_model=UsuarioResponse)
def registrar_usuario(usuario: UsuarioCreate):
    db = SessionLocal()
    try:
        
        usuario_existente = db.query(UsuarioDB).filter(UsuarioDB.username == usuario.username).first()

        if usuario_existente:
            db.close()
            raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")

        hashed_pw = hash_password(usuario.password)

        nuevo_usuario = UsuarioDB(
            username=usuario.username,
            hashed_password=hashed_pw
        )

        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)

        return nuevo_usuario
    
    finally:
        db.close()

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    try:
        usuario_db = (
            db.query(UsuarioDB)
            .filter(UsuarioDB.username == form_data.username)
            .first()
        )

        if not usuario_db:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
            )

        if not verify_password(form_data.password, usuario_db.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
            )

        access_token = create_access_token(data={"sub": usuario_db.username})

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    finally:
        db.close()


@router.get("/me", response_model=UsuarioResponse)
def leer_mi_usuario(usuario_actual: UsuarioDB = Depends(get_current_user)):
    return usuario_actual



    