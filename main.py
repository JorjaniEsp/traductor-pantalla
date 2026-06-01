"""
main.py — Entry point del Traductor de Pantalla
================================================
Uso:
    python main.py

Hotkey: Ctrl + Shift + Q
"""

import threading
import sys
import config  # Carga credenciales de Google al importar

from core.hotkey      import HotkeyListener
from core.capture     import capturar_pantalla, recortar_region
from core.ocr         import extraer_texto
from core.translator  import traducir
from ui.selector      import SelectorPantalla
from ui.result_window import VentanaResultado


def on_region_seleccionada(region):
    """
    Callback que recibe la región recortada del selector.
    Ejecuta OCR + traducción y muestra el resultado.
    """
    try:
        # 1. OCR — Google Vision extrae el texto
        texto = extraer_texto(region)

        if not texto:
            print("[!] No se detectó texto en la zona seleccionada.")
            return

        print(f"[OCR] {texto[:80]}...")

        # 2. Traducción
        traduccion = traducir(texto)
        print(f"[TR]  {traduccion[:80]}...")

        # 3. Mostrar resultado en hilo separado
        threading.Thread(
            target=lambda: VentanaResultado(texto, traduccion),
            daemon=True
        ).start()

    except Exception as e:
        print(f"[ERROR] {e}")


def on_hotkey():
    """
    Callback del hotkey — se ejecuta en el hilo del listener.
    Captura pantalla al instante y abre el selector.
    """
    def _run():
        # Captura INMEDIATA antes de que nada desaparezca
        screenshot = capturar_pantalla()

        # Abre selector sobre la imagen congelada
        SelectorPantalla(screenshot, on_region_seleccionada)

    threading.Thread(target=_run, daemon=True).start()


if __name__ == "__main__":
    print("━" * 50)
    print("  Traductor de Pantalla")
    print("  Hotkey : Ctrl + Shift + Q")
    print("  Salir  : Ctrl + C")
    print("━" * 50)

    listener = HotkeyListener(callback=on_hotkey)
    listener.start()

    try:
        listener.join()
    except KeyboardInterrupt:
        print("\n[·] Cerrando...")
        listener.stop()
        sys.exit(0)
