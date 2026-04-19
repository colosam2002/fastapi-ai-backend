from openai import OpenAI
from fastapi import HTTPException
from knowledge_base import documents
import math

client = OpenAI()

def create_embedding(text: str) -> list[float]:
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )

        return response.data[0].embedding

    except Exception as e:
        print(f"[ERROR EMBEDDING]: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error generando embedding"
        )
    
def generate_all_embeddings():
    for doc in documents:
        if doc["embedding"] is None:
            doc["embedding"] = create_embedding(doc["text"])

def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm_vec1 = math.sqrt(sum(a * a for a in vec1))
    norm_vec2 = math.sqrt(sum(b * b for b in vec2))

    if norm_vec1 == 0 or norm_vec2 == 0:
        return 0.0

    return dot_product / (norm_vec1 * norm_vec2)

def search_similar_documents(query: str, top_k: int = 3):
    query_embedding = create_embedding(query)

    scored_documents = []

    for doc in documents:
        if doc["embedding"] is None:
            continue

        score = cosine_similarity(query_embedding, doc["embedding"])

        scored_documents.append({
            "id": doc["id"],
            "text": doc["text"],
            "score": score
        })

    scored_documents.sort(key=lambda x: x["score"], reverse=True)

    return scored_documents[:top_k]

def get_most_relevant_document(query: str):
    results = search_similar_documents(query, top_k=1)
    return results[0] if results else None

def build_context(results: list[dict]) -> str:
    context_parts = []

    for result in results:
        context_parts.append(
            f"Documento {result['id']}:\n{result['text']}"
        )

    return "\n\n".join(context_parts)


RAG_INSTRUCTIONS = """
Eres un asistente técnico útil y claro.
Responde siempre en español.
Usa principalmente el contexto proporcionado para responder.
Si el contexto no es suficiente, dilo claramente y no inventes información.
Sé preciso y directo.
"""

def answer_with_knowledge(question: str, top_k: int = 3, username : str | None = None) -> dict:
    try:
        results = search_similar_documents(question, top_k=top_k)
        context = build_context(results)

        prompt = f"""
        Contexto:
        {context}

        Pregunta del usuario:
        {question}
        """

        response = client.responses.create(
            model="gpt-5.4-mini",
            instructions=RAG_INSTRUCTIONS,
            input=prompt
        )

        answer = response.output_text

        if not answer or not answer.strip():
            raise HTTPException(
                status_code=500,
                detail="No se pudo generar una respuesta válida"
            )

        return {
            "answer": answer.strip(),
            "sources": results
        }

    except HTTPException:
        raise

    except Exception as e:
        print(f"[ERROR RAG]: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error generando respuesta con contexto"
        )