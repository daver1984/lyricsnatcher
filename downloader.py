"""
Módulo para descargar y extraer audio desde URLs (principalmente YouTube).
Utiliza yt-dlp para descarga y ffmpeg para conversión a formato WAV normalizado.
"""
import os
import tempfile
from pathlib import Path
from typing import Dict, Tuple
import yt_dlp
import shutil

TMP_DIR = Path(__file__).parent / "tmp"

# Localizar ffmpeg en el sistema
FFMPEG_LOCATION = None
ffmpeg_path = shutil.which("ffmpeg")
if ffmpeg_path:
    FFMPEG_LOCATION = str(Path(ffmpeg_path).parent)

def extraer_metadata(info: dict) -> Dict[str, any]:
    """
    Extraer metadatos relevantes de la información del video.
    
    Args:
        info: Diccionario con información del video de yt-dlp
    
    Returns:
        Diccionario con title, artist, album, year
    """
    if not info:
        return {
            'title': 'Desconocido',
            'artist': 'Desconocido',
            'album': None,
            'year': None
        }
    
    title = info.get('title', 'Desconocido')
    
    # Intentar obtener artista del campo 'artist' o 'uploader'
    artist = info.get('artist') or info.get('creator') or info.get('uploader', 'Desconocido')
    
    # Álbum y año pueden no estar disponibles
    album = info.get('album')
    
    # Extraer año de forma segura
    year = None
    if info.get('release_year'):
        year = info.get('release_year')
    elif info.get('upload_date'):
        try:
            year = int(str(info.get('upload_date'))[:4])
        except (ValueError, TypeError):
            year = None
    
    return {
        'title': title,
        'artist': artist,
        'album': album,
        'year': year
    }

def descargar_audio(url: str) -> Tuple[Path, Dict[str, any]]:
    """
    Descargar audio desde URL y convertir a WAV mono 16kHz.
    
    Args:
        url: URL del video (YouTube u otro soportado por yt-dlp)
    
    Returns:
        Tupla (ruta_archivo_audio, metadatos)
    
    Raises:
        Exception: Si falla la descarga o conversión
    """
    # Asegurar que existe el directorio temporal
    TMP_DIR.mkdir(exist_ok=True)
    
    # Generar nombre de archivo temporal único
    temp_id = tempfile.mktemp(prefix='audio_', suffix='', dir=TMP_DIR)
    archivo_salida = Path(temp_id).with_suffix('.wav')
    
    # Configuración de yt-dlp
    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': str(temp_id),
        'quiet': False,  # Mostrar salida para debug
        'no_warnings': False,
        'extract_flat': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
        'postprocessor_args': [
            '-ar', '16000',  # Sample rate 16kHz (óptimo para Whisper)
            '-ac', '1',      # Mono
        ],
    }
    
    # Agregar ubicación de ffmpeg si se encontró
    if FFMPEG_LOCATION:
        opciones['ffmpeg_location'] = FFMPEG_LOCATION
    
    try:
        # Descargar y extraer información
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=True)
            
            if not info:
                raise Exception("No se pudo extraer información del video")
            
            metadata = extraer_metadata(info)
        
        # Verificar que se creó el archivo
        if not archivo_salida.exists():
            raise FileNotFoundError(f"No se pudo crear el archivo de audio: {archivo_salida}")
        
        return archivo_salida, metadata
    
    except yt_dlp.utils.DownloadError as e:
        # Limpiar archivo si existe
        if archivo_salida.exists():
            archivo_salida.unlink()
        raise Exception(f"Error al descargar desde la URL: {str(e)}")
    except Exception as e:
        # Limpiar archivo si existe
        if archivo_salida.exists():
            archivo_salida.unlink()
        raise Exception(f"Error al descargar audio: {str(e)}")

def limpiar_archivo(ruta: Path):
    """
    Eliminar archivo de audio temporal de forma segura.
    
    Args:
        ruta: Path al archivo a eliminar
    """
    try:
        if ruta.exists():
            ruta.unlink()
    except Exception as e:
        print(f"Advertencia: no se pudo eliminar {ruta}: {e}")
