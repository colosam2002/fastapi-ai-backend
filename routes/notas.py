from fastapi import APIRouter, HTTPException, Depends
from models import NotaCreate, NotaResponse
from dependencies import get_current_user

from database import SessionLocal
from models_db import NotaDB, UsuarioDB

router = APIRouter()

@router.post("/notas", response_model=NotaResponse)
def crear_nota(nota: NotaCreate, usuario_actual: UsuarioDB = Depends(get_current_user)):
    db = SessionLocal()

    try:
        nueva_nota = NotaDB(
            titulo=nota.titulo,
            contenido=nota.contenido,
            usuario_id=usuario_actual.id
        )

        db.add(nueva_nota)
        db.commit()
        db.refresh(nueva_nota)

        return nueva_nota
    finally:
        db.close()

@router.get("/notas", response_model=list[NotaResponse])
def listar_mis_notas(usuario_actual: UsuarioDB = Depends(get_current_user)):
    db = SessionLocal()
    try:
        notas = (db.query(NotaDB).filter(NotaDB.usuario_id == usuario_actual.id).all())
        return notas
    
    finally:
        db.close()

@router.get("/notas/{id}", response_model=NotaResponse)
def obtener_nota(id: int, usuario_actual: UsuarioDB = Depends(get_current_user)):
    db = SessionLocal()
    try:
        nota = (db.query(NotaDB).filter(NotaDB.id == id, NotaDB.usuario_id == usuario_actual.id).first())

        if not nota:
            raise HTTPException(status_code=404, detail="Nota no encontrada")

        return nota
    
    finally:
        db.close()

@router.delete("/notas/{id}")
def borrar_nota(id: int, usuario_actual: UsuarioDB = Depends(get_current_user)):

    db = SessionLocal()
    try:
        nota = (db.query(NotaDB).filter(NotaDB.id == id, NotaDB.usuario_id == usuario_actual.id).first())

        if not nota:
            raise HTTPException(
                status_code=404,
                detail="La nota no existe o no te pertenece"
            )

        db.delete(nota)
        db.commit()

        return {"mensaje": "Nota borrada correctamente"}
    
    finally:
        db.close()
