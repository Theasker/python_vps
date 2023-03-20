import requests
import json
import datetime

class YoutubeAPI():

    def __init__(self):
        self._inifile = 'config.json'
        self._channelsFile = 'channels.txt'
        self._urlapi = 'https://www.googleapis.com/youtube/v3'
        self._inivars = {} # Creo un diccionario para las variables del fichero
        self._get_inivars()
        self._youtubeapikey = self._inivars['YOUTUBEAPIKEY']

    def _get_inivars(self):
        try:
            with open(self._inifile, 'r') as file:
                self._inivars = json.load(file)
        except OSError:
            print("Could not open/read file:", fname)
            sys.exit()

    # Devuelve los canales guardados en el fichero de texto
    def _get_channels(self):
        # Leo los canales del fichero de texto
        channels = []

        with open(self._channelsFile, 'r') as file:
            for line in file:
                channels.append(line.strip())

        return channels
    
    # Devuelve los videos del día de un canal
    def _get_youtuve_videos(self):
        for channel in self._get_channels():
            print(channel)
    
    def _get_videos_from_channel(self, channel):
        API_KEY = self._youtubeapikey
        CHANNEL_NAME = channel
        FECHA_INICIO = datetime.datetime(2022, 1, 1).replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + 'Z'
        FECHA_FIN = datetime.datetime(2022, 3, 31).replace(hour=23, minute=59, second=59, microsecond=999999).isoformat() + 'Z'
        MAX_RESULTS = 10


        # Obtener el ID del canal usando la API de búsqueda de canales de YouTube
        busqueda_canal_url = f'https://www.googleapis.com/youtube/v3/search?key={API_KEY}&part=id&type=channel&q={CHANNEL_NAME}'
        # respuesta = request.urlopen(busqueda_canal_url)
        respuesta = requests.get(busqueda_canal_url)
        datos_json = respuesta.json()

        # Obtener el ID de canal a partir de los datos JSON
        canal_id = datos_json['items'][0]['id']['channelId']

        # Obtener los vídeos del canal de youtube entre 2 fechas
        videos_url = f'{self._urlapi}/search?key={API_KEY}&channelId={canal_id}&part=snippet,id&publishedAfter={FECHA_INICIO}&publishedBefore={FECHA_FIN}&type=video&order=date&maxResults={MAX_RESULTS}'
        # Obtener los últimos videos del canal utilizando la API de búsqueda de videos de YouTube
        # videos_url = f'https://www.googleapis.com/youtube/v3/search?key={API_KEY}&channelId={canal_id}&part=snippet,id&order=date&maxResults=1'
        respuesta = requests.get(videos_url)
        #respuesta = request.urlopen(videos_url)
        datos_json = respuesta.json()
 
        # Extraer los datos relevantes de los videos y almacenarlos en una lista
        self._save_json(json.dumps(datos_json['items'][0]))
        
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

if __name__ == "__main__":
    yt = YoutubeAPI()
    
    print(yt._get_videos_from_channel('angel_martin'))
