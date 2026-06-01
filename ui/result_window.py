"""
ui/result_window.py — Ventana de resultado con CustomTkinter
"""

import customtkinter as ctk
import config


class VentanaResultado:
    """
    Ventana minimalista oscura que muestra el texto original
    y su traducción al español.
    """

    def __init__(self, original: str, traduccion: str):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.root = ctk.CTk()
        self.root.title("")
        self.root.resizable(True, True)
        self.root.attributes("-topmost", True)

        # Centrar en pantalla
        w, h = config.UI_WIDTH, config.UI_HEIGHT
        sw   = self.root.winfo_screenwidth()
        sh   = self.root.winfo_screenheight()
        x    = (sw - w) // 2
        y    = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.configure(fg_color=config.COLORS["bg"])

        # Sin bordes nativos
        self.root.overrideredirect(True)

        self._construir_ui(original, traduccion)

        # Cerrar con ESC o Enter
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        self.root.bind("<Return>", lambda e: self.root.destroy())

        self.root.mainloop()

    def _construir_ui(self, original: str, traduccion: str):
        C = config.COLORS

        # ── Barra de título ──────────────────────────────────────────
        title_bar = ctk.CTkFrame(
            self.root,
            fg_color=C["surface"],
            corner_radius=0,
            height=38
        )
        title_bar.pack(fill="x")
        title_bar.pack_propagate(False)

        ctk.CTkLabel(
            title_bar,
            text="  ⬡  Traducción",
            text_color=C["accent"],
            font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"),
            fg_color="transparent"
        ).pack(side="left", padx=4)

        # Botón cerrar
        btn_cerrar = ctk.CTkButton(
            title_bar,
            text="✕",
            width=36, height=28,
            fg_color="transparent",
            hover_color="#3d1f1f",
            text_color=C["text_dim"],
            font=ctk.CTkFont(size=13),
            corner_radius=4,
            command=self.root.destroy
        )
        btn_cerrar.pack(side="right", padx=6, pady=4)

        # Botón copiar traducción
        btn_copiar = ctk.CTkButton(
            title_bar,
            text="⎘  Copiar",
            width=80, height=28,
            fg_color="transparent",
            hover_color=C["border"],
            text_color=C["text_dim"],
            font=ctk.CTkFont(size=11),
            corner_radius=4,
            command=lambda: self._copiar(traduccion)
        )
        btn_copiar.pack(side="right", padx=2, pady=4)

        # Drag para mover ventana
        self._drag_x = self._drag_y = 0
        title_bar.bind("<ButtonPress-1>",  self._start_drag)
        title_bar.bind("<B1-Motion>",      self._do_drag)

        # ── Separador ───────────────────────────────────────────────
        ctk.CTkFrame(
            self.root,
            fg_color=C["border"],
            height=1,
            corner_radius=0
        ).pack(fill="x")

        # ── Cuerpo ──────────────────────────────────────────────────
        body = ctk.CTkFrame(
            self.root,
            fg_color=C["bg"],
            corner_radius=0
        )
        body.pack(fill="both", expand=True, padx=16, pady=12)

        # Label ORIGINAL
        ctk.CTkLabel(
            body,
            text="ORIGINAL",
            text_color=C["text_dim"],
            font=ctk.CTkFont(family="Segoe UI", size=9, weight="bold"),
            fg_color="transparent",
            anchor="w"
        ).pack(fill="x", pady=(0, 4))

        # Caja texto original
        og_box = ctk.CTkTextbox(
            body,
            fg_color=C["surface"],
            text_color=C["text_og"],
            font=ctk.CTkFont(family="Cascadia Code", size=10),
            corner_radius=6,
            border_width=1,
            border_color=C["border"],
            height=90,
            wrap="word",
            activate_scrollbars=False
        )
        og_box.insert("end", original)
        og_box.configure(state="disabled")
        og_box.pack(fill="x", pady=(0, 12))

        # Separador sutil
        ctk.CTkFrame(
            body,
            fg_color=C["border"],
            height=1,
            corner_radius=0
        ).pack(fill="x", pady=(0, 12))

        # Label TRADUCCIÓN
        ctk.CTkLabel(
            body,
            text="TRADUCCIÓN  ·  EN → ES",
            text_color=C["accent"],
            font=ctk.CTkFont(family="Segoe UI", size=9, weight="bold"),
            fg_color="transparent",
            anchor="w"
        ).pack(fill="x", pady=(0, 4))

        # Caja traducción (protagonista)
        tr_box = ctk.CTkTextbox(
            body,
            fg_color=C["surface"],
            text_color=C["text"],
            font=ctk.CTkFont(family="Segoe UI", size=14),
            corner_radius=6,
            border_width=1,
            border_color=C["accent"],
            wrap="word",
            activate_scrollbars=True
        )
        tr_box.insert("end", traduccion)
        tr_box.configure(state="disabled")
        tr_box.pack(fill="both", expand=True)

    def _copiar(self, texto: str):
        self.root.clipboard_clear()
        self.root.clipboard_append(texto)

    def _start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _do_drag(self, event):
        x = self.root.winfo_x() + (event.x - self._drag_x)
        y = self.root.winfo_y() + (event.y - self._drag_y)
        self.root.geometry(f"+{x}+{y}")
