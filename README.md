# Traductor de Pantalla

Herramienta de escritorio para capturar cualquier zona de la pantalla y traducirla al instante al español. Útil para leer documentación técnica, tooltips de código, JavaDoc, y cualquier texto en inglés mientras programás.

## Demo

1. Presionás `Ctrl + Shift + Q`
2. La pantalla se congela — dibujás un rectángulo sobre el texto
3. Aparece la traducción en una ventana minimalista

## Requisitos

- Python 3.10+
- Cuenta de Google Cloud con **Cloud Vision API** habilitada

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/JorjaniEsp/traductor-pantalla.git
cd traductor-pantalla
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar credenciales de Google Cloud

1. Crear un proyecto en [Google Cloud Console](https://console.cloud.google.com)
2. Habilitar la **Cloud Vision API**
3. Crear una cuenta de servicio → descargar clave JSON
4. Renombrar el archivo a `credentials.json` y colocarlo en la raíz del proyecto

> ⚠️ Nunca subas `credentials.json` a git. Ya está incluido en `.gitignore`.

### 4. Correr

```bash
python main.py
```

## Estructura

```
traductor-pantalla/
├── core/
│   ├── hotkey.py        # Listener Ctrl+Shift+Q
│   ├── capture.py       # Captura de pantalla
│   ├── ocr.py           # Google Cloud Vision
│   └── translator.py    # Google Translate (deep-translator)
├── ui/
│   ├── selector.py      # Overlay para seleccionar zona
│   └── result_window.py # Ventana de resultado
├── main.py              # Entry point
├── config.py            # Configuración central
├── credentials.json     # ← no se sube a git
├── .gitignore
├── requirements.txt
└── README.md
```

## Tecnologías

| Componente | Tecnología |
|---|---|
| OCR | Google Cloud Vision API |
| Traducción | deep-translator (Google Translate) |
| Interfaz | CustomTkinter |
| Hotkey | pynput |
| Captura | Pillow (ImageGrab) |

## Licencia

MIT © JorjaniEsp
