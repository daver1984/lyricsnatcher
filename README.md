# 🎵 LyricSnatcher

Sistema web para transcribir y traducir letras de canciones desde URLs de video (principalmente YouTube).

## 📋 Descripción

LyricSnatcher descarga el audio de un video, lo transcribe usando OpenAI Whisper (detección automática de idioma) y traduce el texto al idioma deseado. Guarda las letras y metadatos en una base de datos local para reutilización.

## ✨ Características

- 🎬 Descarga audio desde YouTube y otras plataformas (yt-dlp)
- 🎤 Transcripción automática con Whisper (modelo: small por defecto)
- 🌍 Traducción a español, inglés y portugués
- 💾 Almacenamiento de letras y metadatos en SQLite
- 🔄 Cache automático: no reprocesa URLs ya transcritas
- 🧹 Limpieza automática de archivos temporales
- 🌐 Interfaz web simple y responsive

## 🛠️ Requisitos

- Python 3.10-3.13
- ffmpeg (instalado y en PATH del sistema)
- Conexión a internet (para descarga y traducción online)

## 📦 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/daver1984/lyricsnatcher.git
cd lyricsnatcher
```

### 2. Crear entorno virtual

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Linux/Mac
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Instalar ffmpeg

**Windows:**
```powershell
# Con winget
winget install ffmpeg

# Con Chocolatey
choco install ffmpeg

# Con Scoop
scoop install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Mac:**
```bash
brew install ffmpeg
```

Verificar instalación:
```bash
ffmpeg -version
```

## 🚀 Uso

### Iniciar el servidor

```bash
python app.py
```

El servidor se ejecutará en `http://localhost:8000`

### Opción 1: Interfaz web

1. Abre `index.html` en tu navegador
2. Pega la URL del video de YouTube
3. Selecciona el idioma de traducción
4. Haz clic en "Transcribir y Traducir"
5. Espera 3-5 minutos (proceso completo)

### Opción 2: API directa

```bash
curl -X POST http://localhost:8000/transcribe-translate \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.youtube.com/watch?v=EJEMPLO",
    "target_lang": "es"
  }'
```

**Idiomas soportados:** `es` (español), `en` (inglés), `pt` (portugués)

### Opción 3: Script de prueba

```bash
# Editar test_api.py con la URL deseada
python test_api.py
```

## 📁 Estructura del Proyecto

```
lyricsnatcher/
├── app.py                      # API FastAPI principal
├── database.py                 # Módulo SQLite (tabla lyrics)
├── downloader.py              # Descarga audio con yt-dlp
├── translator.py              # Traducción (LibreTranslate/Argos)
├── transcriber/
│   └── whisper_transcriber.py # Transcripción con Whisper
├── index.html                 # Interfaz web
├── test_api.py               # Script de prueba
├── requirements.txt          # Dependencias Python
├── tmp/                      # Archivos temporales (auto-limpieza)
├── data/
│   └── lyrics.sqlite        # Base de datos de letras
└── .gitignore
```

## 🔧 Configuración Avanzada

### Variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# Modelo Whisper (tiny, base, small, medium, large)
WHISPER_MODEL=small

# URL del servicio LibreTranslate (opcional)
LIBRETRANSLATE_URL=https://libretranslate.de
```

### Cambiar puerto del servidor

Edita `app.py`:

```python
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)
```

## 🗄️ Base de Datos

La tabla `lyrics` almacena:

- `id`: ID autoincremental
- `title`: Título de la canción
- `artist`: Artista/banda
- `album`: Álbum (opcional)
- `year`: Año (opcional)
- `source_url`: URL original del video
- `language_src`: Idioma detectado por Whisper
- `language_dst`: Idioma de traducción
- `text_src`: Letra original transcrita
- `text_dst`: Letra traducida
- `created_at`: Timestamp de creación

## 🌐 API Endpoints

### `GET /`
Información de la API

### `GET /health`
Health check del servidor

### `POST /transcribe-translate`

**Request:**
```json
{
  "url": "https://www.youtube.com/watch?v=EJEMPLO",
  "target_lang": "es"
}
```

**Response:**
```json
{
  "title": "Nombre de la canción",
  "artist": "Artista",
  "album": "Álbum",
  "year": 2023,
  "source_url": "https://...",
  "language_src": "en",
  "language_dst": "es",
  "text_src": "Letra original...",
  "text_dst": "Letra traducida..."
}
```

## ⚠️ Notas Importantes

- ⏱️ El proceso completo puede tardar 3-5 minutos por canción
- 🔊 Solo se descarga y procesa el audio (no el video completo)
- 🧹 Los archivos de audio se eliminan automáticamente después del procesamiento
- 💾 Solo se almacenan letras y metadatos (cumplimiento legal)
- 🌐 La primera traducción puede tardar más (descarga de modelos Argos)

## 🐛 Solución de Problemas

### Error: "ffmpeg not found"
- Instala ffmpeg y asegúrate de que esté en el PATH del sistema
- En Windows, reinicia PowerShell después de instalar

### Error: "Timeout"
- Videos muy largos pueden exceder el timeout
- Intenta con videos más cortos o aumenta el timeout en `test_api.py`

### Error de traducción
- El sistema usa LibreTranslate (online) con fallback a Argos (offline)
- Si ambos fallan, verifica conexión a internet
- La primera vez descarga modelos de Argos (puede tardar)

## 📝 TODO / Mejoras Futuras

- [ ] Soporte para más idiomas
- [ ] Interfaz web mejorada con historial
- [ ] Exportar letras a .txt, .pdf, .srt
- [ ] Sistema de colas para múltiples solicitudes
- [ ] Docker / contenedor para deployment
- [ ] Detección de múltiples idiomas en una canción
- [ ] Timestamps de sincronización de letra

## 📄 Licencia

Este proyecto es de código abierto para fines educativos. 

**Importante:** Este sistema solo almacena transcripciones de texto. No almacena ni redistribuye contenido de audio/video original.

## 👤 Autor

**Dante Verdugo**
- GitHub: [@daver1984](https://github.com/daver1984)

## 🙏 Agradecimientos

- [OpenAI Whisper](https://github.com/openai/whisper) - Transcripción
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Descarga de audio
- [LibreTranslate](https://libretranslate.com/) - Traducción online
- [Argos Translate](https://github.com/argosopentech/argos-translate) - Traducción offline
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web
