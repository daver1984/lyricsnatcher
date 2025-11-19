"""
Módulo de base de datos SQLite para almacenar letras y metadatos.
"""
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

DB_PATH = Path(__file__).parent / "data" / "lyrics.sqlite"

def inicializar_base_datos():
    """Crear tabla de letras si no existe."""
    # Asegurar que el directorio data/ existe
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lyrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            album TEXT,
            year INTEGER,
            source_url TEXT NOT NULL UNIQUE,
            language_src TEXT NOT NULL,
            language_dst TEXT NOT NULL,
            text_src TEXT NOT NULL,
            text_dst TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conexion.commit()
    conexion.close()

def guardar_letra(datos: Dict[str, Any]) -> int:
    """
    Guardar letra transcrita y traducida en la base de datos.
    
    Args:
        datos: Diccionario con campos title, artist, album, year, source_url,
               language_src, language_dst, text_src, text_dst
    
    Returns:
        ID del registro insertado
    """
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    
    cursor.execute("""
        INSERT INTO lyrics (title, artist, album, year, source_url, 
                           language_src, language_dst, text_src, text_dst)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datos["title"],
        datos["artist"],
        datos.get("album"),
        datos.get("year"),
        datos["source_url"],
        datos["language_src"],
        datos["language_dst"],
        datos["text_src"],
        datos["text_dst"]
    ))
    
    id_registro = cursor.lastrowid
    conexion.commit()
    conexion.close()
    
    return id_registro

def buscar_por_url(url: str) -> Optional[Dict[str, Any]]:
    """
    Buscar letra existente por URL de origen.
    
    Args:
        url: URL del video/audio original
    
    Returns:
        Diccionario con datos de la letra o None si no existe
    """
    conexion = sqlite3.connect(DB_PATH)
    conexion.row_factory = sqlite3.Row
    cursor = conexion.cursor()
    
    cursor.execute("SELECT * FROM lyrics WHERE source_url = ?", (url,))
    resultado = cursor.fetchone()
    
    conexion.close()
    
    if resultado:
        return dict(resultado)
    return None

# Inicializar base de datos al importar el módulo
inicializar_base_datos()
