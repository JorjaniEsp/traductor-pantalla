"""
core/tray.py — Ícono en la barra del sistema
"""

import threading
from PIL import Image, ImageDraw
import pystray
from core.autostart import esta_habilitado, habilitar, deshabilitar


def _crear_icono() -> Image.Image:
    size = 64
    img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([4, 4, size - 4, size - 4], fill="#4ade80")
    draw.rectangle([24, 18, 40, 22], fill="white")
    draw.rectangle([29, 18, 35, 48], fill="white")
    return img


class TrayIcon:

    def __init__(self, on_salir):
        self.on_salir = on_salir
        self._icon    = None

    def start(self):
        threading.Thread(target=self._run, daemon=True).start()

    def _run(self):
        def toggle_autostart(icon, item):
            if esta_habilitado():
                deshabilitar()
            else:
                habilitar()
            # Actualizar el menú
            icon.menu = self._construir_menu()
            icon.update_menu()

        self._icon = pystray.Icon(
            name="traductor-pantalla",
            icon=_crear_icono(),
            title="Traductor de Pantalla",
            menu=self._construir_menu()
        )
        self._icon.run()

    def _construir_menu(self):
        autostart_label = (
            "✓ Iniciar con Windows"
            if esta_habilitado()
            else "  Iniciar con Windows"
        )
        return pystray.Menu(
            pystray.MenuItem("Traductor de Pantalla", None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Ctrl + Shift + Q  →  Traducir", None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(autostart_label, self._toggle_autostart),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Salir", self._salir),
        )

    def _toggle_autostart(self, icon, item):
        if esta_habilitado():
            deshabilitar()
        else:
            habilitar()
        icon.menu = self._construir_menu()
        icon.update_menu()

    def _salir(self, icon, item):
        icon.stop()
        self.on_salir()

    def stop(self):
        if self._icon:
            self._icon.stop()
