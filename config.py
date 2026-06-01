"""
config.py — Configuración central del proyecto
"""

import os
from pathlib import Path

# ─── RUTAS ────────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent
CREDENTIALS_PATH = BASE_DIR / "credentials.json"

# Apuntamos Google Cloud al archivo de credenciales
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(CREDENTIALS_PATH)

# ─── HOTKEY ───────────────────────────────────────────────────────────────────

# Combinación de teclas para activar la captura
# Ctrl + Shift + Q
HOTKEY_CTRL  = True
HOTKEY_SHIFT = True
HOTKEY_KEY   = 'q'

# ─── OCR ──────────────────────────────────────────────────────────────────────

# Idioma del texto a extraer (en = inglés)
OCR_LANGUAGE = "en"

# ─── TRADUCCIÓN ───────────────────────────────────────────────────────────────

TRANSLATE_SOURCE = "auto"   # Detecta automáticamente el idioma
TRANSLATE_TARGET = "es"     # Español

# ─── INTERFAZ ─────────────────────────────────────────────────────────────────

# Tema de la ventana de resultado
UI_THEME      = "dark"
UI_WIDTH      = 580
UI_HEIGHT     = 480

# Paleta de colores
COLORS = {
    "bg":       "#1a1d23",
    "surface":  "#22262f",
    "border":   "#2e333d",
    "accent":   "#4ade80",
    "text":     "#e2e8f0",
    "text_dim": "#8892a4",
    "text_og":  "#64748b",
    "error":    "#ff6b6b",
}
