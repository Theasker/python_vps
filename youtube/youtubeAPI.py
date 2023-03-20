import requests
import json
import datetime
import os
import configparser
import subprocess
import re

class YoutubeAPI():
    def __init__(self):
        # Read local file `config.ini`.
        self._config = configparser.ConfigParser() 
        self._config.read('/usr/src/app/youtube/config.ini')
        self._channelsFile = '/usr/src/app/youtube/channels.txt'
        self._urlapi = 'https://www.googleapis.com/youtube/v3'
        self._youtubeapikey = self._config['YOUTUBE']['APIKEY']
        """
        self._inifile = "config.json"
        self._inivars = {} # Creo un diccionario para las variables del fichero
        self._get_inivars()
        self._youtubeapikey = self._inivars['YOUTUBEAPIKEY']
        """
    """
    def _get_inivars(self):
        try:
            with open(self._inifile, 'r') as file:
                self._inivars = json.load(file)

        except OSError:
            print("Could not open/read file:", fname)
            sys.exit()
    """

    # Devuelve los canales guardados en el fichero de texto
    def _get_channels(self):
        # Leo los canales del fichero de texto
        channels = []

        with open(self._channelsFile, 'r') as file:
            for line in file:
                channels.append(line.strip())

        return channels
    
    # Devuelve los videos del día de un canal
    def _get_videos_from_channel(self, channel_id):
        API_KEY = self._youtubeapikey
        CHANNEL_NAME = channel_id
        FECHA_INICIO = datetime.datetime(2023, 3, 15).replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
        #FECHA_FIN = datetime.datetime(2023, 3, 31).replace(hour=23, minute=59, second=59, microsecond=999999).isoformat() + 'Z'
        MAX_RESULTS = 10
        
        """
        # Obtener el ID del canal usando la API de búsqueda de canales de YouTube
        busqueda_canal_url = f'{self._urlapi}/search?key={API_KEY}&part=id&type=channel&q={CHANNEL_NAME}'
        # respuesta = request.urlopen(busqueda_canal_url)
        respuesta = requests.get(busqueda_canal_url)
        datos_json = respuesta.json()

        # Obtener el ID de canal a partir de los datos JSON
        canal_id = datos_json['items'][0]['id']['channelId']
        """

        # Obtener los vídeos del canal de youtube desde una fechas
        videos_url = f'{self._urlapi}/search?key={API_KEY}&channelId={channel_id}&part=snippet,id&publishedAfter={FECHA_INICIO}&type=video&order=date&maxResults={MAX_RESULTS}'

        # Obtener los últimos videos del canal utilizando la API de búsqueda de videos de YouTube
        # videos_url = f'https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={canal_id}&part=snippet,id&order=date&maxResults=1'
    
        respuesta = requests.get(videos_url)
        datos_json = respuesta.json()
        print(datos_json)
 
        # Extraer los datos relevantes de los videos y almacenarlos en una lista
        #self._save_json(json.dumps(datos_json['items'][0]))
        
        videos = []
        for resultado in datos_json['items']:
            if resultado['id']['kind'] == 'youtube#video':
                video = {
                    'canal': CHANNEL_NAME,
                    'titulo': resultado['snippet']['title'],
                    'descripcion': resultado['snippet']['description'],
                    'id_video': resultado['id']['videoId'],
                    'fecha': resultado['snippet']['publishedAt'],
                }
                videos.append(video)
        return videos

    def _save_json(self, text):
        file = open('temp.json','w+')
        file.write(text)
        file.close()
    
    def download_from_channels(self):
        channels = self._get_channels()
        for ch in channels:
            print(f"{ch} => ")
    
    def pruebas(self):
        # Define la URL del canal de YouTube
        url = "https://www.youtube.com/channel/UCo5HJNjfdSoPWsdAHLsvSxQ"

        # Extrae el ID del canal de la URL utilizando una expresión regular
        match = re.search(r"channel\/(.{24})", url)
        channel_id = match.group(1)
        print(channel_id)

        # Define los parámetros de la solicitud
        params = {
            "part": "snippet",
            "id": channel_id,
            "key": self._youtubeapikey
        }

        # Realiza la solicitud a la API de YouTube
        response = requests.get("https://www.googleapis.com/youtube/v3/channels", params=params)

        # Analiza la respuesta de la API de YouTube
        data = json.loads(response.text)
        print(data)
        channel_name = data["items"][0]["snippet"]["title"]

        # Imprime el ID y el nombre del canal
        print(f"ID del canal: {channel_id}")
        print(f"Nombre del canal: {channel_name}")

    def _get_channelID_from_channelURL(self, channel):
        # Define los parámetros de la solicitud de búsqueda
        params = {
            "part": "id",
            "type": "channel",
            "q": channel,
            "key": self._youtubeapikey
        }

        # Realiza la solicitud de búsqueda a la API de YouTube
        response = requests.get("https://www.googleapis.com/youtube/v3/search", params=params)
        

        
        # Analiza la respuesta de la API de YouTube
        data = json.loads(response.text)        
        channel_id = data["items"][0]["id"]["channelId"]

        # Imprime el ID del canal
        return channel_id
        

if __name__ == "__main__":
    yt = YoutubeAPI()
    # yt.download_from_channels()
    print(yt._get_channelID_from_channelURL("https://www.youtube.com/@MauriSegura"))

    

