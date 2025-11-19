"""
Aplicación principal FastAPI para lyricsnatcher.
Sistema de transcripción y traducción de letras desde URLs de video.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional, Literal
import os

app = FastAPI(
    title="LyricSnatcher",
    description="API para transcripción y traducción de letras desde URLs de video",
    version="0.1.0"
)

# Configurar CORS para permitir peticiones desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de datos
class SolicitudTranscripcion(BaseModel):
    """Modelo de entrada para solicitud de transcripción y traducción."""
    url: HttpUrl
    target_lang: Literal["es", "en", "pt"]

class RespuestaTranscripcion(BaseModel):
    """Modelo de respuesta con letra transcrita y traducida."""
    title: str
    artist: str
    album: Optional[str] = None
    year: Optional[int] = None
    source_url: str
    language_src: str
    language_dst: str
    text_src: str
    text_dst: str

@app.get("/")
async def raiz():
    """Endpoint raíz con información de la API."""
    return {
        "app": "LyricSnatcher",
        "version": "0.1.0",
        "descripcion": "API para transcripción y traducción de letras",
        "endpoints": {
            "POST /transcribe-translate": "Transcribir y traducir letra desde URL"
        }
    }

@app.get("/health")
async def health_check():
    """Verificar estado de la API."""
    return {"status": "ok", "message": "API funcionando correctamente"}

@app.post("/transcribe-translate", response_model=RespuestaTranscripcion)
async def transcribir_y_traducir(solicitud: SolicitudTranscripcion):
    """
    Endpoint principal: descarga audio, transcribe y traduce.
    
    Flujo:
    1. Validar URL
    2. Descargar audio (temporal)
    3. Transcribir con Whisper
    4. Traducir al idioma objetivo
    5. Guardar metadatos y letra
    6. Limpiar archivos temporales
    """
    # TODO: Implementar lógica completa
    # Por ahora, respuesta de prueba
    raise HTTPException(
        status_code=501,
        detail="Endpoint en desarrollo. Próximamente: descarga, transcripción y traducción."
    )

if __name__ == "__main__":
    import uvicorn
    # Crear directorios necesarios
    os.makedirs("tmp", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    
    # Ejecutar servidor
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
