"""
core/autostart.py — Autostart con Windows
Agrega o elimina el programa del inicio de Windows via registro.
"""

import sys
import winreg
from pathlib import Path


APP_NAME = "TraductorPantalla"
PYTHON   = sys.executable
SCRIPT   = str(Path(__file__).parent.parent / "main.py")
COMANDO  = f'"{PYTHON}" "{SCRIPT}"'
REG_KEY  = r"Software\Microsoft\Windows\CurrentVersion\Run"


def esta_habilitado() -> bool:
    """Verifica si el autostart está activo."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_KEY) as key:
            winreg.QueryValueEx(key, APP_NAME)
            return True
    except FileNotFoundError:
        return False


def habilitar():
    """Agrega el programa al inicio de Windows."""
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_KEY, 0, winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, COMANDO)
    print("[·] Autostart habilitado.")


def deshabilitar():
    """Elimina el programa del inicio de Windows."""
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_KEY, 0, winreg.KEY_SET_VALUE) as key:
            winreg.DeleteValue(key, APP_NAME)
        print("[·] Autostart deshabilitado.")
    except FileNotFoundError:
        pass
