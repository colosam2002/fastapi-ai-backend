# FastAPI AI Backend

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/fastapi-ai-backend.git
cd fastapi-ai-backend
```
### 2. Create a Virtual Environment
Linux / macOS / WSL
```bash
python -m venv venv
source venv/bin/activate
```
Windows
```bash
python -m venv venv
venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure Environment Variables

Create a .env file in the project root:

OPENAI_API_KEY=your_api_key_here
DATABASE_URL=postgresql://user:password@localhost/database_name
SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

### 5. Create PostgreSQL Database

Make sure PostgreSQL is installed and create a database.

```SQL
CREATE DATABASE api_db;
```

### 6. Run the Application
```bash
uvicorn main:app --reload
```

The API will be available at:

http://127.0.0.1:8000

Interactive Swagger documentation:

http://127.0.0.1:8000/docs

## What This Project Does

This project is a FastAPI backend that combines a traditional API architecture with modern AI-powered features.

### Full Backend System
- User registration
- JWT authentication login
- Notes management per user
- Protected private endpoints

### AI Features

#### /ask

Allows users to ask general questions to the model.

Example request:

{
  "question": "What is FastAPI?"
}

#### /copilot

Receives a text and returns:

Summary
Improved version
Improvement suggestions

Example request:

{
  "text": "My original text..."
}

#### /knowledge/search

Semantic search system over internal texts using embeddings.

Finds relevant information based on meaning, not only keyword matching.

#### /knowledge/ask

Basic RAG system:

- Receives a question
- Searches relevant texts using embeddings
- Uses those texts as context
- Generates a context-aware answer


### Technologies Used
- Python 3.12+
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT Authentication
- Passlib / bcrypt
- OpenAI API
- Embeddings
- Semantic Search
- Basic RAG


### Project Structure
fastapi-ai-backend/
│
├── main.py
├── auth.py
├── database.py
├── dependencies.py
├── models.py
├── models_db.py
├── ai_service.py
├── rag_service.py
├── knowledge_base.py
├── requirements.txt
└── routes/
    │ 
    ├── usuarios.py
    ├── notas.py
    ├── knowledge.py
    ├── copilot.py
    └── ask.py

### Future Improvements
- Frontend UI instead of relying only on /docs
- File upload per user
- Embedding persistence
- Vector database (pgvector)
- User-specific RAG
- Cloud deployment

### Author

Project developed as part of a practical roadmap focused on backend engineering + applied AI systems.