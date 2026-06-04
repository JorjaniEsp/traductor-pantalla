"""
ui/result_window.py — Ventana de resultado (PyQt6)
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QFrame, QApplication
)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui  import QPainter, QColor, QShortcut, QKeySequence, QFontMetrics, QFont
import config


def _calcular_alto(texto: str, font_size: int, ancho: int, max_alto: int, padding: int = 20) -> int:
    """Calcula el alto necesario para mostrar el texto completo."""
    font    = QFont("Segoe UI", font_size)
    metrics = QFontMetrics(font)
    line_h  = metrics.lineSpacing()
    chars_per_line = max(1, (ancho - padding * 2) // max(1, metrics.averageCharWidth()))
    lineas  = 0
    for parrafo in texto.split("\n"):
        if not parrafo:
            lineas += 1
        else:
            lineas += max(1, (len(parrafo) // chars_per_line) + 1)
    alto = lineas * line_h + padding * 2
    return min(alto, max_alto)


class VentanaResultado(QWidget):

    def __init__(self, original: str, traduccion: str):
        super().__init__()
        self._drag_pos = QPoint()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedWidth(config.UI_WIDTH)

        self._construir_ui(original, traduccion)

        # Centrar
        self.adjustSize()
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width()  - self.width())  // 2,
            (screen.height() - self.height()) // 2
        )
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(0, 0, 0, 60))
        painter.drawRoundedRect(self.rect().adjusted(4, 4, 4, 4), 12, 12)
        painter.setBrush(QColor(config.COLORS["bg"]))
        painter.drawRoundedRect(self.rect().adjusted(0, 0, -4, -4), 12, 12)

    def _construir_ui(self, original: str, traduccion: str):
        C          = config.COLORS
        ancho_util = config.UI_WIDTH - 64  # descontando márgenes

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 4, 4)
        layout.setSpacing(0)

        # ── Título ───────────────────────────────────────────────
        title_bar = QWidget()
        title_bar.setFixedHeight(42)
        title_bar.setStyleSheet(f"""
            background-color: {C['surface']};
            border-radius: 12px 12px 0px 0px;
        """)
        tl = QHBoxLayout(title_bar)
        tl.setContentsMargins(14, 0, 8, 0)

        lbl_titulo = QLabel("⬡  Traducción")
        lbl_titulo.setStyleSheet(f"""
            color: {C['accent']};
            font-family: 'Segoe UI';
            font-size: 13px;
            font-weight: bold;
            background: transparent;
        """)

        btn_copiar = QPushButton("⎘  Copiar")
        btn_copiar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_copiar.setStyleSheet(f"""
            QPushButton {{
                color: {C['text_dim']};
                background: transparent;
                border: 1px solid {C['border']};
                border-radius: 5px;
                padding: 3px 10px;
                font-size: 11px;
                font-family: 'Segoe UI';
            }}
            QPushButton:hover {{
                background: {C['border']};
                color: {C['text']};
            }}
        """)
        btn_copiar.clicked.connect(lambda: QApplication.clipboard().setText(traduccion))

        btn_cerrar = QPushButton("✕")
        btn_cerrar.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_cerrar.setFixedSize(28, 28)
        btn_cerrar.setStyleSheet(f"""
            QPushButton {{
                color: {C['text_dim']};
                background: transparent;
                border: none;
                border-radius: 5px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background: #3d1f1f;
                color: #ff6b6b;
            }}
        """)
        btn_cerrar.clicked.connect(self.close)

        tl.addWidget(lbl_titulo)
        tl.addStretch()
        tl.addWidget(btn_copiar)
        tl.addSpacing(6)
        tl.addWidget(btn_cerrar)

        title_bar.mousePressEvent = self._start_drag
        title_bar.mouseMoveEvent  = self._do_drag
        layout.addWidget(title_bar)

        # ── Separador ────────────────────────────────────────────
        sep = QFrame()
        sep.setFixedHeight(1)
        sep.setStyleSheet(f"background: {C['border']};")
        layout.addWidget(sep)

        # ── Cuerpo ───────────────────────────────────────────────
        body = QWidget()
        body.setStyleSheet(f"background: {C['bg']};")
        bl = QVBoxLayout(body)
        bl.setContentsMargins(16, 12, 16, 16)
        bl.setSpacing(8)

        # Original
        lbl_og = QLabel("ORIGINAL")
        lbl_og.setStyleSheet(f"""
            color: {C['text_dim']};
            font-size: 9px;
            font-weight: bold;
            font-family: 'Segoe UI';
            letter-spacing: 1px;
            background: transparent;
        """)
        bl.addWidget(lbl_og)

        og_alto = _calcular_alto(original, 10, ancho_util, max_alto=120)
        og_box  = QTextEdit()
        og_box.setPlainText(original)
        og_box.setReadOnly(True)
        og_box.setFixedHeight(og_alto)
        og_box.setStyleSheet(f"""
            QTextEdit {{
                background: {C['surface']};
                color: {C['text_og']};
                font-family: 'Cascadia Code', 'Consolas';
                font-size: 11px;
                border: 1px solid {C['border']};
                border-radius: 6px;
                padding: 8px;
            }}
            QScrollBar:vertical {{
                background: {C['surface']};
                width: 6px;
                border-radius: 3px;
            }}
            QScrollBar::handle:vertical {{
                background: {C['border']};
                border-radius: 3px;
            }}
        """)
        bl.addWidget(og_box)

        sep2 = QFrame()
        sep2.setFixedHeight(1)
        sep2.setStyleSheet(f"background: {C['border']};")
        bl.addWidget(sep2)

        # Traducción
        lbl_tr = QLabel("TRADUCCIÓN  ·  EN → ES")
        lbl_tr.setStyleSheet(f"""
            color: {C['accent']};
            font-size: 9px;
            font-weight: bold;
            font-family: 'Segoe UI';
            letter-spacing: 1px;
            background: transparent;
        """)
        bl.addWidget(lbl_tr)

        tr_alto = _calcular_alto(traduccion, 13, ancho_util, max_alto=300, padding=24)
        tr_box  = QTextEdit()
        tr_box.setPlainText(traduccion)
        tr_box.setReadOnly(True)
        tr_box.setFixedHeight(tr_alto)
        tr_box.setStyleSheet(f"""
            QTextEdit {{
                background: {C['surface']};
                color: {C['text']};
                font-family: 'Segoe UI';
                font-size: 13px;
                border: 1px solid {C['accent']};
                border-radius: 6px;
                padding: 10px;
            }}
            QScrollBar:vertical {{
                background: {C['surface']};
                width: 6px;
                border-radius: 3px;
            }}
            QScrollBar::handle:vertical {{
                background: {C['border']};
                border-radius: 3px;
            }}
        """)
        bl.addWidget(tr_box)
        layout.addWidget(body)

        QShortcut(QKeySequence("Escape"), self).activated.connect(self.close)
        QShortcut(QKeySequence("Return"), self).activated.connect(self.close)

    def _start_drag(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def _do_drag(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)


class VentanaError(QWidget):

    def __init__(self, mensaje: str):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(340, 120)

        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width()  - 340) // 2,
            (screen.height() - 120) // 2
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)

        lbl = QLabel(mensaje)
        lbl.setWordWrap(True)
        lbl.setStyleSheet(f"""
            color: {config.COLORS['error']};
            font-family: 'Segoe UI';
            font-size: 12px;
            background: transparent;
        """)
        layout.addWidget(lbl)

        btn = QPushButton("Cerrar")
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {config.COLORS['surface']};
                color: {config.COLORS['text']};
                border: none;
                border-radius: 5px;
                padding: 6px;
                font-family: 'Segoe UI';
                font-size: 11px;
            }}
            QPushButton:hover {{ background: {config.COLORS['border']}; }}
        """)
        btn.clicked.connect(self.close)
        layout.addWidget(btn)

        QShortcut(QKeySequence("Escape"), self).activated.connect(self.close)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(config.COLORS["bg"]))
        painter.drawRoundedRect(self.rect(), 10, 10)
