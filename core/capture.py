"""
core/capture.py — Captura instantánea de pantalla completa
"""

from PIL import ImageGrab, Image


def capturar_pantalla() -> Image.Image:
    """
    Captura la pantalla completa al instante.
    Se llama justo al presionar el hotkey, antes de
    que cualquier ventana se abra y los tooltips desaparezcan.
    """
    return ImageGrab.grab()


def recortar_region(screenshot: Image.Image, x1: int, y1: int, x2: int, y2: int) -> Image.Image:
    """
    Recorta una región de la screenshot completa.
    Las coordenadas vienen del selector de pantalla.
    """
    return screenshot.crop((x1, y1, x2, y2))
