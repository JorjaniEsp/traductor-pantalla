"""
ui/selector.py — Overlay con pantalla congelada para seleccionar región
"""

import tkinter as tk
from PIL import Image, ImageTk


class SelectorPantalla:
    """
    Muestra la screenshot completa como fondo congelado.
    El usuario dibuja un rectángulo sobre la zona que quiere traducir.
    Al soltar el mouse llama al callback con la región recortada.
    """

    def __init__(self, screenshot: Image.Image, callback):
        self.screenshot = screenshot
        self.callback   = callback
        self.start_x    = 0
        self.start_y    = 0
        self.rect       = None
        self.scale_x    = 1.0
        self.scale_y    = 1.0

        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.config(cursor="crosshair")

        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        # Factor de escala por si el monitor es HiDPI
        self.scale_x = screenshot.width  / sw
        self.scale_y = screenshot.height / sh

        # Redimensionar screenshot al tamaño exacto de la pantalla
        img_display = screenshot.resize((sw, sh), Image.LANCZOS)
        self.tk_img  = ImageTk.PhotoImage(img_display)

        self.canvas = tk.Canvas(
            self.root,
            width=sw, height=sh,
            highlightthickness=0,
            cursor="crosshair"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Fondo: screenshot congelada
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

        # Overlay oscuro semitransparente
        self.canvas.create_rectangle(
            0, 0, sw, sh,
            fill="black",
            stipple="gray25",
            outline=""
        )

        # Instrucción centrada arriba
        self.canvas.create_text(
            sw // 2, 28,
            text="Seleccioná la zona a traducir   •   ESC para cancelar",
            fill="#ffffff",
            font=("Segoe UI", 12),
            anchor="n"
        )

        self.canvas.bind("<ButtonPress-1>",   self._on_press)
        self.canvas.bind("<B1-Motion>",       self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self.root.bind("<Escape>", lambda e: self.root.destroy())

        self.root.mainloop()

    def _on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)

    def _on_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y,
            outline="#ffffff",
            width=2,
            dash=(6, 3)
        )

    def _on_release(self, event):
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)
        self.root.destroy()

        if (x2 - x1) < 10 or (y2 - y1) < 10:
            return  # Selección muy pequeña, ignorar

        # Convertir coordenadas de pantalla a coordenadas reales del screenshot
        rx1 = int(x1 * self.scale_x)
        ry1 = int(y1 * self.scale_y)
        rx2 = int(x2 * self.scale_x)
        ry2 = int(y2 * self.scale_y)

        region = self.screenshot.crop((rx1, ry1, rx2, ry2))
        self.callback(region)
