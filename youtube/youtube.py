import os
import yt_dlp
from datetime import datetime

# Ruta al archivo que contiene la lista de canales de YouTube
ruta_archivo_canales = "lista_canales.txt"

# Obtener la lista de canales de YouTube del archivo
with open(ruta_archivo_canales, "r") as archivo:
    lista_canales = archivo.read().splitlines()

# Opciones de yt-dlp
# "bestvideo+bestaudio/best"
# "bestvideo[height<=720]+bestaudio/best[height<=720]"
# "format": "worstvideo+worstaudio"
# Opciones de yt-dlp
fecha_actual = datetime.today().strftime('%Y%m%d')
opciones = {
    "format": "bestvideo[height<=720]+bestaudio/best[height<=720]",
    "daterange": fecha_actual,
    '%(channel)s/%(title)s.%(ext)s'
    "outtmpl": os.path.join(carpeta_salida, "%(upload_date)s_%(uploader)s_%(title)s.%(ext)s")
}

# Carpeta donde se guardarán los videos descargados
carpeta_salida = "./videos/"

# Crear la carpeta de salida si no existe
if not os.path.exists(carpeta_salida):
    os.makedirs(carpeta_salida)

# Descargar los videos de cada canal
for canal in lista_canales:
    with yt_dlp.YoutubeDL(opciones) as ydl:
        ydl.download([canal])
        print("Se descargaron los videos de", canal)
