"""
Módulo de transcripción usando OpenAI Whisper.
Detecta idioma automáticamente y transcribe audio a texto.
"""
import whisper
import os
from pathlib import Path
from typing import Dict

# Modelo por defecto (puede cambiarse con variable de entorno)
MODELO_WHISPER = os.getenv('WHISPER_MODEL', 'small')

# Cache del modelo cargado
_modelo_cache = None

def cargar_modelo():
    """
    Cargar modelo Whisper (usa cache para no recargar).
    
    Returns:
        Modelo Whisper cargado
    """
    global _modelo_cache
    if _modelo_cache is None:
        _modelo_cache = whisper.load_model(MODELO_WHISPER)
    return _modelo_cache

def transcribir_audio(ruta_audio: Path) -> Dict[str, str]:
    """
    Transcribir archivo de audio usando Whisper.
    
    Args:
        ruta_audio: Path al archivo de audio (WAV 16kHz mono)
    
    Returns:
        Diccionario con 'text' (transcripción) y 'language' (idioma detectado)
    
    Raises:
        Exception: Si falla la transcripción
    """
    if not ruta_audio.exists():
        raise FileNotFoundError(f"Archivo de audio no encontrado: {ruta_audio}")
    
    try:
        modelo = cargar_modelo()
        
        # Transcribir con detección automática de idioma
        resultado = modelo.transcribe(
            str(ruta_audio),
            fp16=False,  # Usar FP32 para compatibilidad (FP16 requiere GPU CUDA)
            language=None,  # Detección automática
            task='transcribe'  # Transcribir (no traducir aquí)
        )
        
        return {
            'text': resultado['text'].strip(),
            'language': resultado['language']
        }
    
    except Exception as e:
        raise Exception(f"Error en transcripción Whisper: {str(e)}")