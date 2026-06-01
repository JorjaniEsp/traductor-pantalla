"""
core/translator.py — Traducción con deep-translator (Google Translate gratis)
"""

from deep_translator import GoogleTranslator
import config


def traducir(texto: str) -> str:
    """
    Recibe un texto en cualquier idioma y devuelve
    su traducción al español.
    """

    if not texto or not texto.strip():
        return ""

    # deep-translator maneja textos largos automáticamente
    traduccion = GoogleTranslator(
        source=config.TRANSLATE_SOURCE,
        target=config.TRANSLATE_TARGET
    ).translate(texto)

    return traduccion or ""
