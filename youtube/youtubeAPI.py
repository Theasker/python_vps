import requests
import json
import datetime
import os
import configparser
import logging
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
        self.LOGFILE = self._config['YOUTUBE']['LOGFILE']
        # Configuro el loggin 
        logger = logging.getLogger(__name__)
        logging.basicConfig(
            filename=self.LOGFILE, 
            encoding='utf-8', 
            level=logging.INFO,
            format='%(asctime)s:  %(name)s: %(levelname)s: %(message)s', 
            datefmt='%Y/%m/%d %H:%M:%S'
        )
        self.logger = logging.getLogger(__name__)
        self.truncate_file(self.LOGFILE)
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
    
    # Devuelve los videos del día de un canal desde una fecha dada
    def _get_videos_from_channel(self, channel_id, after_date):

        API_KEY = self._youtubeapikey
        CHANNEL_NAME = channel_id
        # FECHA_INICIO = datetime.datetime(2023, 3, 15).replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
        FECHA_INICIO = datetime.datetime(after_date.year, after_date.month, after_date.day).replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
        #FECHA_FIN = datetime.datetime(2023, 3, 31).replace(hour=23, minute=59, second=59, microsecond=999999).isoformat() + 'Z'
        print(FECHA_INICIO)
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
        print(f"channel_id: {channel_id} ({len(videos)} vídeos)")
        return videos

    def _save_json(self, text):
        file = open('temp.json','w+')
        file.write(text)
        file.close()
    
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
        
        res = json.loads(response.content)      

        if (len(res['items']) == 0):
            print("No hay resultados")
            return None
        else:
            # Analiza la respuesta de la API de YouTube
            data = json.loads(response.text)        
            channel_id = data["items"][0]["id"]["channelId"]

            # Imprime el ID del canal
            return channel_id

    def _get_last_date(self):
        # Leer la fecha del archivo de texto
        with open('date.txt', 'r') as filedate:
            last_date = filedate.read()
        # Convertir la cadena de texto en un objeto datetime
        # last_date_obj = datetime.datetime.strptime(last_date, '%Y-%m-%d %H:%M:%S.%f')
        last_date_obj = datetime.datetime.strptime(last_date, '%Y-%m-%d')
        # print(f"{last_date} ({type(last_date)}) => {last_date_obj} ({type(last_date_obj)})")
        # Obtener la fecha actual
        now_date = datetime.datetime.now()
        # Escribir la fecha en un archivo de texto
        with open('date.txt', 'w') as filedate:
            date_str = now_date.strftime('%Y-%m-%d')
            filedate.write(date_str)
        # Devolvemos la fecha del fichero como objeto fecha
        return last_date_obj

    def download_from_channels(self):
        channels = self._get_channels()
        self.logger.info(channels)
        # Get the last date saved
        after_date = self._get_last_date()
        for ch in channels:
            print(f"Channel: {ch}")
            # Get the channel id
            channel_id = self._get_channelID_from_channelURL(ch)
            # print(f"{ch} => {channel_id}")
            videos = self._get_videos_from_channel(channel_id, after_date)
            # print(videos)        

    def truncate_file(self, file):
        try:
            with open(file, "r+") as f:
                f.truncate(0)
        except FileNotFoundError:
            print('El archivo no existe')
        except:
            print('Ocurrió un error')

if __name__ == "__main__":
    yt = YoutubeAPI()
    # yt.download_from_channels()
    # print(yt._get_channelID_from_channelURL("https://www.youtube.com/@MauriSegura"))

    

