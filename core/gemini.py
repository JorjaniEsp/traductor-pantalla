"""
core/gemini.py — OCR + Traducción en una sola llamada con Gemini Flash
"""

import io
import os
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODELO = "gemini-2.5-flash"

PROMPT_TRADUCCION = """Tu única responsabilidad es extraer el texto de esta imagen y traducirlo al español.

Reglas estrictas:
- Si no hay texto en la imagen, devuelve exactamente: ""
- No agregues explicaciones, saludos, ni comentarios
- No uses markdown, asteriscos ni formato especial
- Devuelve únicamente el texto traducido, tal como aparece en la imagen pero en español
- Mantené la estructura y saltos de línea del texto original"""

PROMPT_ORIGINAL = """Extraé únicamente el texto de esta imagen, sin traducir.
Si no hay texto devuelve exactamente: ""
Sin explicaciones ni formato extra."""


def _imagen_a_bytes(imagen: Image.Image) -> bytes:
    buffer = io.BytesIO()
    imagen.save(buffer, format="PNG")
    return buffer.getvalue()


def extraer_y_traducir(imagen: Image.Image) -> tuple[str, str]:
    """
    Recibe una imagen PIL.
    Devuelve (texto_original, texto_traducido).
    """
    img_bytes = _imagen_a_bytes(imagen)

    parte_imagen = types.Part.from_bytes(
        data=img_bytes,
        mime_type="image/png"
    )

    # Llamada 1 — Traducción
    respuesta_tr = cliente.models.generate_content(
        model=MODELO,
        contents=[PROMPT_TRADUCCION, parte_imagen],
        config=types.GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=2048,
        )
    )
    traduccion = respuesta_tr.text.strip()

    if traduccion == '""' or not traduccion:
        return "", ""

    # Llamada 2 — Original
    respuesta_og = cliente.models.generate_content(
        model=MODELO,
        contents=[PROMPT_ORIGINAL, parte_imagen],
        config=types.GenerateContentConfig(
            temperature=0.1,
            max_output_tokens=2048,
        )
    )
    original = respuesta_og.text.strip()
    if original == '""':
        original = ""

    return original, traduccion
