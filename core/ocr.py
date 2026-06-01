"""
core/ocr.py — Extracción de texto con Google Cloud Vision
"""

import io
from PIL import Image
from google.cloud import vision
import config


def extraer_texto(imagen: Image.Image) -> str:
    """
    Recibe una imagen PIL, la envía a Google Cloud Vision
    y devuelve el texto extraído como string limpio.
    """

    # Convertir imagen PIL a bytes
    buffer = io.BytesIO()
    imagen.save(buffer, format="PNG")
    contenido = buffer.getvalue()

    # Crear cliente de Vision
    cliente = vision.ImageAnnotatorClient()

    # Construir objeto imagen para la API
    imagen_vision = vision.Image(content=contenido)

    # Hacer la petición OCR
    respuesta = cliente.text_detection(image=imagen_vision)

    # Verificar errores de la API
    if respuesta.error.message:
        raise RuntimeError(f"Error de Google Vision: {respuesta.error.message}")

    anotaciones = respuesta.text_annotations

    # La primera anotación contiene TODO el texto detectado
    if not anotaciones:
        return ""

    texto = anotaciones[0].description.strip()
    return texto
