import requests
import json
import time

# Esperar un momento para asegurar que el servidor esté listo
time.sleep(2)

url_video = "https://www.youtube.com/watch?v=zbQOBRUOhGs"

print("\n" + "="*60)
print("PROBANDO LYRICSNATCHER")
print("="*60)
print(f"URL: {url_video}")
print("Idioma destino: Español")
print("\nProcesando (puede tomar 3-5 minutos)...")
print("Fases: descarga -> transcripción -> traducción\n")

try:
    respuesta = requests.post(
        "http://localhost:8000/transcribe-translate",
        json={
            "url": url_video,
            "target_lang": "es"
        },
        timeout=600
    )
    
    if respuesta.status_code == 200:
        datos = respuesta.json()
        print("\n" + "="*60)
        print("RESULTADO EXITOSO")
        print("="*60)
        print(f"\nCanción: {datos['title']}")
        print(f"Artista: {datos['artist']}")
        print(f"Álbum: {datos.get('album', 'N/A')}")
        print(f"Año: {datos.get('year', 'N/A')}")
        print(f"Idioma detectado: {datos['language_src']}")
        print(f"\nLongitud texto original: {len(datos['text_src'])} caracteres")
        print(f"Longitud traducción: {len(datos['text_dst'])} caracteres")
        print(f"\n--- MUESTRA TEXTO ORIGINAL ({datos['language_src'].upper()}) ---")
        print(datos['text_src'][:200] + "...")
        print(f"\n--- MUESTRA TRADUCCIÓN ({datos['language_dst'].upper()}) ---")
        print(datos['text_dst'][:200] + "...")
        print("\n" + "="*60)
        print("PRUEBA COMPLETADA CON ÉXITO")
        print("="*60 + "\n")
    else:
        error = respuesta.json()
        print(f"\nERROR {respuesta.status_code}: {error.get('detail', 'Error desconocido')}")
        
except requests.exceptions.ConnectionError:
    print("\nERROR: No se pudo conectar al servidor. Asegúrate de que está corriendo en http://localhost:8000")
except requests.exceptions.Timeout:
    print("\nERROR: Timeout - el proceso tomó más de 10 minutos")
except Exception as e:
    print(f"\nERROR: {e}")
