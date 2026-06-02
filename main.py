"""
main.py — Entry point del Traductor de Pantalla
"""

import sys
import threading
import config

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore    import QObject, pyqtSignal
from PIL             import Image

from core.hotkey      import HotkeyListener
from core.capture     import capturar_pantalla
from core.gemini      import extraer_y_traducir
from ui.selector      import SelectorPantalla
from ui.result_window import VentanaResultado, VentanaError

_screenshot_pendiente = None


class Coordinador(QObject):
    senal_mostrar_resultado = pyqtSignal(str, str)
    senal_error             = pyqtSignal(str)


coordinador = Coordinador()


def on_region_seleccionada(region: Image.Image):
    """Corre en hilo del selector — procesa con Gemini."""
    def _procesar():
        try:
            print("[·] Procesando con Gemini...")
            original, traduccion = extraer_y_traducir(region)

            if not traduccion:
                coordinador.senal_error.emit("No se detectó texto en la zona seleccionada.")
                return

            print("[OK] Traducción lista.")
            coordinador.senal_mostrar_resultado.emit(original, traduccion)

        except Exception as e:
            print(f"[ERROR] {e}")
            coordinador.senal_error.emit(f"Error: {str(e)}")

    threading.Thread(target=_procesar, daemon=True).start()


def on_hotkey():
    """Corre en hilo del listener — captura y abre selector en hilo propio."""
    def _run():
        print("[·] Capturando pantalla...")
        screenshot = capturar_pantalla()
        # Selector corre en su propio hilo con tkinter
        SelectorPantalla(screenshot, on_region_seleccionada)

    threading.Thread(target=_run, daemon=True).start()


def mostrar_resultado(original: str, traduccion: str):
    """Corre en hilo principal Qt."""
    VentanaResultado(original, traduccion)


def mostrar_error(mensaje: str):
    """Corre en hilo principal Qt."""
    VentanaError(mensaje)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    coordinador.senal_mostrar_resultado.connect(mostrar_resultado)
    coordinador.senal_error.connect(mostrar_error)

    listener = HotkeyListener(callback=on_hotkey)
    listener.start()

    print("━" * 50)
    print("  Traductor de Pantalla")
    print("  Hotkey : Ctrl + Shift + Q")
    print("  Salir  : Ctrl + C")
    print("━" * 50)

    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        print("\n[·] Cerrando...")
        listener.stop()
        sys.exit(0)
