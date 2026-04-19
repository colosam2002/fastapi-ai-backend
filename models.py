from pydantic import BaseModel, Field

class UsuarioCreate(BaseModel):
    username: str
    password: str

class UsuarioLogin(BaseModel):
    username: str
    password: str

class UsuarioResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class NotaCreate(BaseModel):
    titulo:str
    contenido:str

class NotaResponse(BaseModel):
    id: int
    titulo: str
    contenido: str
    usuario_id: int

    class Config:
        from_attributes = True

class AskRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=500
    )

class AskResponse(BaseModel):
    answer: str


class CopilotRequest(BaseModel):
    text: str = Field(min_length=1, max_length=3000)

class CopilotResponse(BaseModel):
    summary: str
    improved_text: str
    suggestions: list[str]

class KnowledgeDocumentResult(BaseModel):
    id: int
    text: str
    score: float

class KnowledgeSearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    top_k: int = Field(default=3, ge=1, le=5)

class KnowledgeSearchResponse(BaseModel):
    results: list[KnowledgeDocumentResult]

class KnowledgeAskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=500)
    top_k: int = Field(default=3, ge=1, le=5)

class KnowledgeAskResponse(BaseModel):
    answer: str
    sources: list[KnowledgeDocumentResult]