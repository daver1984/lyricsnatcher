"""
Módulo de traducción con fallback entre LibreTranslate y Argos Translate.
Prioridad: LibreTranslate (online) → Argos Translate (offline).
"""
import os
from typing import Optional

# Intentar importar servicios de traducción
try:
    from libretranslatepy import LibreTranslateAPI
    LIBRETRANSLATE_DISPONIBLE = True
except ImportError:
    LIBRETRANSLATE_DISPONIBLE = False

try:
    import argostranslate.package
    import argostranslate.translate
    ARGOS_DISPONIBLE = True
except ImportError:
    ARGOS_DISPONIBLE = False

# Configuración LibreTranslate
LIBRETRANSLATE_URL = os.getenv('LIBRETRANSLATE_URL', 'https://libretranslate.com')

# Mapeo de códigos de idioma
CODIGO_IDIOMA = {
    'es': 'Spanish',
    'en': 'English', 
    'pt': 'Portuguese'
}

def traducir_con_libretranslate(texto: str, idioma_origen: str, idioma_destino: str) -> Optional[str]:
    """
    Traducir usando LibreTranslate API.
    
    Args:
        texto: Texto a traducir
        idioma_origen: Código de idioma origen (es, en, pt)
        idioma_destino: Código de idioma destino (es, en, pt)
    
    Returns:
        Texto traducido o None si falla
    """
    if not LIBRETRANSLATE_DISPONIBLE:
        return None
    
    try:
        lt = LibreTranslateAPI(LIBRETRANSLATE_URL)
        resultado = lt.translate(texto, idioma_origen, idioma_destino)
        return resultado
    except Exception as e:
        print(f"Error en LibreTranslate: {e}")
        return None

def traducir_con_argos(texto: str, idioma_origen: str, idioma_destino: str) -> Optional[str]:
    """
    Traducir usando Argos Translate (offline).
    
    Args:
        texto: Texto a traducir
        idioma_origen: Código de idioma origen (es, en, pt)
        idioma_destino: Código de idioma destino (es, en, pt)
    
    Returns:
        Texto traducido o None si falla
    """
    if not ARGOS_DISPONIBLE:
        return None
    
    try:
        # Actualizar índice de paquetes (solo primera vez)
        argostranslate.package.update_package_index()
        paquetes_disponibles = argostranslate.package.get_available_packages()
        
        # Buscar paquete de traducción
        paquete = next(
            (p for p in paquetes_disponibles 
             if p.from_code == idioma_origen and p.to_code == idioma_destino),
            None
        )
        
        if paquete is None:
            print(f"Paquete Argos {idioma_origen}→{idioma_destino} no disponible")
            return None
        
        # Descargar e instalar si no está instalado
        if not paquete.is_installed():
            argostranslate.package.install_from_path(paquete.download())
        
        # Traducir
        texto_traducido = argostranslate.translate.translate(texto, idioma_origen, idioma_destino)
        return texto_traducido
    
    except Exception as e:
        print(f"Error en Argos Translate: {e}")
        return None

def traducir_texto(texto: str, idioma_origen: str, idioma_destino: str) -> str:
    """
    Traducir texto con fallback automático entre servicios.
    
    Args:
        texto: Texto a traducir
        idioma_origen: Código de idioma origen (es, en, pt, auto-detectado de Whisper)
        idioma_destino: Código de idioma destino (es, en, pt)
    
    Returns:
        Texto traducido
    
    Raises:
        Exception: Si todos los servicios fallan
    """
    # Si el idioma origen y destino son iguales, retornar texto original
    if idioma_origen == idioma_destino:
        return texto
    
    # Intentar LibreTranslate primero
    resultado = traducir_con_libretranslate(texto, idioma_origen, idioma_destino)
    if resultado:
        return resultado
    
    # Fallback a Argos Translate
    resultado = traducir_con_argos(texto, idioma_origen, idioma_destino)
    if resultado:
        return resultado
    
    # Si ambos fallan
    raise Exception(
        f"No se pudo traducir de {idioma_origen} a {idioma_destino}. "
        f"LibreTranslate disponible: {LIBRETRANSLATE_DISPONIBLE}, "
        f"Argos disponible: {ARGOS_DISPONIBLE}"
    )
