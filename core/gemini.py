"""
core/gemini.py — OCR + Traducción en una sola llamada optimizada
"""

import io
import os
from google import genai
from google.genai import types
from PIL import Image
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

cliente = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODELO      = "gemini-2.5-flash"
MAX_ANCHO   = 800   # px — suficiente para cualquier texto legible
JPEG_QUALITY = 75   # balance velocidad / precisión OCR


class ResultadoTraduccion(BaseModel):
    original: str
    traduccion: str


PROMPT = """Analiza la imagen provista.
1. Extraé el texto original exactamente como aparece, sin traducir.
2. Traducí ese mismo texto al español.
Si la imagen no contiene texto legible, devolvé cadenas vacías."""


def _imagen_a_bytes(imagen: Image.Image) -> bytes:
    """
    Prepara la imagen para enviar a Gemini:
    1. Reduce resolución si es muy grande (menos datos = más rápido)
    2. Convierte a escala de grises (el color no aporta al OCR)
    3. Comprime como JPEG quality=75
    """
    # 1. Reducir si supera el ancho máximo
    if imagen.width > MAX_ANCHO:
        ratio     = MAX_ANCHO / imagen.width
        nuevo_alto = int(imagen.height * ratio)
        imagen    = imagen.resize((MAX_ANCHO, nuevo_alto), Image.LANCZOS)

    # 2. Escala de grises — 3x menos peso que RGB
    imagen = imagen.convert("L")

    # 3. Comprimir
    buffer = io.BytesIO()
    imagen.save(buffer, format="JPEG", quality=JPEG_QUALITY)
    return buffer.getvalue()


def extraer_y_traducir(imagen: Image.Image) -> tuple[str, str]:
    """
    Recibe una imagen PIL.
    Devuelve (texto_original, texto_traducido) en una sola llamada a Gemini.
    """
    img_bytes = _imagen_a_bytes(imagen)

    parte_imagen = types.Part.from_bytes(
        data=img_bytes,
        mime_type="image/jpeg"
    )

    respuesta = cliente.models.generate_content(
        model=MODELO,
        contents=[PROMPT, parte_imagen],
        config=types.GenerateContentConfig(
            temperature=0.1,
            response_mime_type="application/json",
            response_schema=ResultadoTraduccion,
        )
    )

    datos = ResultadoTraduccion.model_validate_json(respuesta.text)
    return datos.original, datos.traduccion
