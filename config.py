"""
config.py — Configuración central del proyecto
"""

from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# ─── RUTAS ────────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent

# ─── GEMINI ───────────────────────────────────────────────────────────────────

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ─── INTERFAZ ─────────────────────────────────────────────────────────────────

UI_WIDTH  = 580
UI_HEIGHT = 480

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
