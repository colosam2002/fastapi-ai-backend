API de notas con autenticación JWT.

-Tecnologías
FastAPI
PostgreSQL
SQLAlchemy
JWT

-Funcionalidades
registro
login
usuario actual
CRUD parcial de notas protegidas por usuario

-Cómo ejecutar
crear entorno virtual
instalar dependencias
arrancar uvicorn


Semana 5: 
Nombre del proyecto

Mini copiloto de texto

Qué hace

Recibe un texto y devuelve:

resumen
versión mejorada
sugerencias
Qué no hace
no traduce
no responde preguntas sobre el texto
no añade información inventada
no guarda historial todavía
Público objetivo

Usuarios autenticados de tu API que quieren mejorar un texto rápidamente.

Meta de la semana

Construir una versión estable, clara y demostrable.

Nombre

Mini Copilot API

Qué hace

Recibe un texto y devuelve:

resumen
versión mejorada
3 sugerencias
Tecnologías
FastAPI
PostgreSQL
JWT
OpenAI API
Endpoint principal

POST /copilot

Seguridad

Solo usuarios autenticados pueden usarlo.

Proyecto 1: API con FastAPI, PostgreSQL y JWT que integra varias capacidades de IA:

/ask: preguntas generales al modelo
/copilot: resumen, mejora y sugerencias sobre un texto
/knowledge/search: búsqueda semántica sobre textos propios usando embeddings
/knowledge/ask: sistema RAG básico que responde usando contexto recuperado

los embeddings se generan con text-embedding-3-small, 
modelo recomendado para embeddings por OpenAI, y se usan para búsqueda semántica; 
luego la respuesta se genera con la Responses API.