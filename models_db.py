from sqlalchemy import Column, Integer, String
from database import engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class UsuarioDB(Base):
    __tablename__="usuarios"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    notas = relationship("NotaDB", back_populates="usuario")

class NotaDB(Base):
    __tablename__="notas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    contenido = Column(String)

    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    usuario = relationship("UsuarioDB", back_populates="notas")
