from fastapi import FastAPI
from routes.notas import router as notas_router
from routes.usuarios import router as usuarios_router
from routes.ask import router as ask_router
from routes.copilot import router as copilot_router
from routes.knowledge import router as knowledge_router

from models_db import Base
from database import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(notas_router)
app.include_router(usuarios_router)
app.include_router(ask_router)
app.include_router(copilot_router)
app.include_router(knowledge_router)

@app.get("/")
def read_root():
    return {"mensaje": "API Funcionando"}
