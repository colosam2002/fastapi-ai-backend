from openai import OpenAI
from fastapi import HTTPException
import json
from json import JSONDecodeError
from pydantic import ValidationError

from models import CopilotResponse

import os
from dotenv import load_dotenv

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI()

INSTRUCTIONS = """
Eres un asistente técnico útil y claro.
Responde siempre en español.
Explica conceptos de programación y desarrollo de software de forma sencilla.
Sé preciso y directo.
Usa ejemplos pequeños cuando ayuden.
No inventes información si no estás seguro.
No alargues la respuesta innecesariamente.
No superes 5-6 líneas de texto.
"""

COPILOT_INSTRUCTIONS = """
Eres un asistente especializado en mejorar textos.
Responde siempre en español.

Tu tarea es:
1. Resumir el texto en 1 a 3 frases.
2. Reescribirlo de forma más clara y fluida.
3. Dar exactamente 3 sugerencias concretas y accionables.

Reglas:
- Conserva siempre el significado original.
- No inventes información nueva.
- No elimines ideas importantes.
- Mejora claridad, estructura y redacción.
- Evita sugerencias genéricas.
- Devuelve exactamente las claves summary, improved_text y suggestions.
"""

def ask_model(question: str, username: str | None = None) -> str:
    try:
        instructions = INSTRUCTIONS

        if username:
            instructions += f"\nEl usuario actual se llama {username}."

        response = client.responses.create(
            model="gpt-5.4-mini",
            instructions=instructions,
            input=question
        )

        answer = response.output_text

        if not answer or answer.strip() == "":
            answer = "No he podido generar una respuesta válida."

        return answer

    except Exception as e:
        print(f"[ERROR OPENAI]: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al procesar la solicitud con IA"
        )
    
def run_copilot(text: str, username: str | None = None) -> CopilotResponse:
    try:

        instructions=COPILOT_INSTRUCTIONS

        if username:
            instructions += f"\nEl usuario actual se llama {username}"

        response = client.responses.create(
            model="gpt-5.4-mini",
            instructions=instructions,
            input=text,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "copilot_response",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "summary": {"type": "string"},
                            "improved_text": {"type": "string"},
                            "suggestions": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 3,
                                "maxItems": 3
                            }
                        },
                        "required": ["summary", "improved_text", "suggestions"],
                        "additionalProperties": False
                    }
                }
            }
        )

        output_text = response.output_text

        if not output_text or not output_text.strip():
            raise HTTPException(
                status_code=500,
                detail="El copiloto no devolvió contenido"
            )

        parsed_data = json.loads(output_text)

        validated_data = CopilotResponse(**parsed_data)

        if not validated_data.summary.strip():
            raise HTTPException(
                status_code=500,
                detail="El copiloto devolvió un resumen vacío"
            )

        if not validated_data.improved_text.strip():
            raise HTTPException(
                status_code=500,
                detail="El copiloto devolvió un texto mejorado vacío"
            )

        cleaned_suggestions = []
        for suggestion in validated_data.suggestions:
            cleaned = suggestion.strip()
            if not cleaned:
                raise HTTPException(
                    status_code=500,
                    detail="El copiloto devolvió una sugerencia vacía"
                )
            cleaned_suggestions.append(cleaned)

        if len(cleaned_suggestions) != 3:
            raise HTTPException(
                status_code=500,
                detail="El copiloto no devolvió exactamente 3 sugerencias"
            )

        if len(set(cleaned_suggestions)) != 3:
            raise HTTPException(
                status_code=500,
                detail="El copiloto devolvió sugerencias repetidas"
            )

        return CopilotResponse(
            summary=validated_data.summary.strip(),
            improved_text=validated_data.improved_text.strip(),
            suggestions=cleaned_suggestions
        )

    except HTTPException:
        raise

    except JSONDecodeError as e:
        print(f"[ERROR COPILOT JSON]: {e}")
        raise HTTPException(
            status_code=500,
            detail="El copiloto devolvió un JSON inválido"
        )

    except ValidationError as e:
        print(f"[ERROR COPILOT VALIDATION]: {e}")
        raise HTTPException(
            status_code=500,
            detail="El copiloto devolvió una estructura inválida"
        )

    except Exception as e:
        print(f"[ERROR COPILOT OPENAI]: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al procesar el texto con el copiloto"
        )