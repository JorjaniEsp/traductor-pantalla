# Traductor de Pantalla

Herramienta de escritorio para capturar cualquier zona de la pantalla y traducirla al instante al español. Útil para leer documentación técnica, tooltips de código, JavaDoc, y cualquier texto en inglés mientras programás.

## ¿Cómo funciona?

1. Presionás `Ctrl + Shift + Q`
2. La pantalla se congela — dibujás un rectángulo sobre el texto
3. Gemini extrae el texto y lo traduce en una sola llamada
4. Aparece la traducción en una ventana minimalista

## Requisitos

- Python 3.10+
- API Key de Google AI Studio (gratuita, sin tarjeta de crédito)

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

### 3. Obtener API Key de Gemini

1. Entrá a [aistudio.google.com](https://aistudio.google.com)
2. Iniciá sesión con tu cuenta de Google
3. Clic en **"Get API key"** → **"Create API key"**
4. Seleccioná el proyecto **"Default Gemini Project"**
5. Copiá la key generada

### 4. Configurar credenciales

Creá un archivo `.env` en la raíz del proyecto:

```
GEMINI_API_KEY=tu-api-key-acá
```

> ⚠️ Nunca subas el archivo `.env` a git. Ya está incluido en `.gitignore`.

### 5. Correr

```bash
python main.py
```

El programa queda corriendo en segundo plano escuchando el hotkey.

## Uso

| Acción | Resultado |
|---|---|
| `Ctrl + Shift + Q` | Activa la captura |
| Dibujá un rectángulo | Seleccioná la zona a traducir |
| `ESC` | Cancelar selección |
| `ESC` o `Enter` | Cerrar ventana de traducción |
| Botón **⎘ Copiar** | Copia la traducción al portapapeles |
| `Ctrl + C` en terminal | Cerrar el programa |

## Estructura

```
traductor-pantalla/
├── core/
│   ├── hotkey.py        # Listener Ctrl+Shift+Q
│   ├── capture.py       # Captura instantánea de pantalla
│   └── gemini.py        # OCR + Traducción con Gemini Flash
├── ui/
│   ├── selector.py      # Overlay para seleccionar zona (tkinter)
│   └── result_window.py # Ventana de resultado (PyQt6)
├── main.py              # Entry point
├── config.py            # Configuración central
├── .env                 # ← API key, no se sube a git
├── .gitignore
├── requirements.txt
└── README.md
```

## Tecnologías

| Componente | Tecnología |
|---|---|
| OCR + Traducción | Google Gemini Flash (una sola llamada) |
| Selector de zona | tkinter |
| Ventana de resultado | PyQt6 |
| Hotkey global | pynput |
| Captura de pantalla | Pillow (ImageGrab) |

## Límites gratuitos

Gemini Flash en el tier gratuito de AI Studio incluye **1,500 requests por día** sin tarjeta de crédito. Para uso personal traduciendo documentación y tooltips mientras programás, es más que suficiente.

## Licencia

MIT © JorjaniEsp
