# Instrucciones para agentes de IA – lyricsnatcher

Objetivo
- Web para pegar una URL (principalmente YouTube), transcribir con Whisper y traducir a español/inglés/portugués. Guardar solo la letra y metadatos (título/artista/URL). Eliminar siempre audio/vídeo temporales.

Arquitectura (alto nivel)
- Downloader: descargar audio desde URL con yt-dlp y extraer pista con ffmpeg (temporal, carpeta `tmp/`).
- Transcriber (`transcriber/`): usar OpenAI Whisper (modelo por defecto: `small`) para idioma detectado automáticamente.
- Translator: usar servicio libre. Preferencia: 1) LibreTranslate (HTTP API), 2) Argos Translate (offline). Evitar dependencias pagas.
- Backend (sugerido): FastAPI + Uvicorn. Endpoint principal: POST /transcribe-translate { url, target_lang }.
- Frontend: formulario simple (URL + selector de idioma) que muestra la traducción.
- Persistencia: almacenar letra y metadatos (no medios). Sugerido: SQLite (tabla `lyrics`).

Flujo esencial (pipeline)
1) Validar URL → 2) Descargar/extraer audio (16 kHz mono) → 3) Transcribir con Whisper → 4) Traducir → 5) Guardar texto+metadatos → 6) Borrar archivos temporales.

Convenciones del proyecto
- Todo en español: nombres de variables/funciones, docstrings y UI.
- Estructura actual: `transcriber/` (Whisper), `audio/` (muestras), `requirements.txt` (whisper, torch, ffmpeg-python).
- No subir medios al repositorio. Usar `tmp/` para archivos temporales y limpiar en `finally`.

Contratos API (propuesta inicial)
- Entrada: { url: string, target_lang: "es"|"en"|"pt" }
- Respuesta: { title, artist, album?, year?, source_url, language_src, language_dst, text_src, text_dst }
	- artist: nombre del intérprete o banda
	- album: opcional si se puede inferir (YouTube muchas veces no provee este dato)
	- year: opcional (a completar manualmente en futura versión si no se obtiene del origen)
- Errores: 400 (URL inválida), 422 (traducción no soportada), 500 (fallo descarga/transcripción).

Dependencias y requisitos
- Python 3.10+. Requiere ffmpeg instalado y en PATH. En Windows: verificar `ffmpeg -version`.
- Paquetes actuales: openai-whisper, torch, ffmpeg-python. Próximos: yt-dlp, libretranslate (cliente) o argos-translate.
- GPU opcional (PyTorch con CUDA acelera Whisper si está disponible).

Workflows de desarrollo
- Preparar entorno: crear venv e instalar `requirements.txt`; añadir paquetes nuevos si se aprueban.
- Prueba rápida: usar `audio/sample.wav` para validar transcripción local antes de integrar descarga.
- Verificación: asegurar que se eliminan archivos de `tmp/` tras cada solicitud.

Decisiones técnicas preferidas
- Whisper modelo `small` por defecto; permitir cambiar vía variable de entorno.
- Descargar solo audio; normalizar a WAV mono 16 kHz.
- Traducción: intentar LibreTranslate (configurable por URL de servicio); si no, Argos Translate offline.
- Persistencia mínima: SQLite con tabla `lyrics(id, title, artist, album, year, source_url, language_src, language_dst, text_src, text_dst, created_at)`.
- Campos opcionales (`album`, `year`) pueden quedar NULL si no se determinan.

Notas de cumplimiento
- No almacenar audio/vídeo originales. Registrar únicamente texto y metadatos. Borrar temporales de inmediato.
- `tmp/` sólo debe contener archivos intermedios (WAV normalizado). Limpiar siempre en bloque `finally`.
- Evitar conservar hashes ni fragmentos del audio original.

Rutas y almacenamiento
- Desarrollo local (actual): usar carpetas `tmp/` y `data/` dentro del root del proyecto (`C:/Users/dverd/OneDrive/Documentos/Project/lyricsnatcher`).
- `data/lyrics.sqlite` archivo persistente para letras y metadatos.
- Producción (futuro): `tmp/` debería ser almacenamiento efímero (RAM disk / volumen temporal del contenedor) y `data/lyrics.sqlite` migrará a una base más robusta si escala.
- No es viable usar el equipo del cliente para procesar audio en esta etapa (se hará en servidor); si en el futuro se hace client-side, habría que cambiar el pipeline.

Archivos clave actuales
- `transcriber/whisper_transcriber.py` (a implementar), `transcriber/__init__.py`, `audio/sample.wav`, `requirements.txt`.
