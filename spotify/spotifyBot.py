import configparser
import logging
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
sys.path.append("..")
from telegramBot.telegramBot import TelegramBot
import subprocess

class Spotify(TelegramBot):
    def __init__(self, url):
        # Leo las variables de entorno del fichero de configuración
        config = configparser.ConfigParser() 
        config.read('/usr/src/app/spotify/config.ini')
        self.LOGFILE = config['SPOTIFY']['LOGFILE']
        self.BOT_TOKEN = config['SPOTIFY']['TELEGRAMBOTTOKEN']
        self.CLIENTID = config['SPOTIFY']['CLIENTID']
        self.CLIENTSECRET = config['SPOTIFY']['CLIENTSECRET']
        # Carga el token del bot en la clase heredada
        # super().__init__(self._inivars['TELEGRAMBOTTOKEN'])
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
        self.logger.info(url)
        # Creo el objeto spotify
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=self.CLIENTID, client_secret=self.CLIENTSECRET))
        self._dispatch(url)

    def temp(self, user):
        us = self.sp.user(user)
        print(us)

    def _dispatch(self, url):
        tracks = []
        if ('playlist' in url):
            playlistid = self._getid(url)
            self.get_playlistInfo(playlistid)
            tracks = self.get_playlistTracks(playlistid)
        elif ('track' in url):
            print('track')
        elif ('album' in url):
            album = self._getid(url)
            self.get_album(album)
        #print(json.dumps(tracks))

    def _getid(self, url):
        urlsplit = url.split("/")
        dirt_id = urlsplit[len(urlsplit) - 1]
        array_id = dirt_id.split("?")
        id = array_id[0]
        return id

    # Obtiene las playlist del usuario
    def get_userPlaylists(self, username):
        playlists = self.sp.user_playlists(username)
        # print(json.dumps(playlists['items'][0]))

        arrayPlaylists = []
         
        for playlist in playlists['items']:
            # print(playlist['name'])
            pl = {
                "name": playlist['name'],
                "spotifyurl": playlist['external_urls']['spotify'],
                "playlist_id": playlist['id']
            }
            arrayPlaylists.append(pl)
        return arrayPlaylists

    # Obtiene todos los datos de una playlist
    def get_playlistInfo(self, playlistid):
        playlist = self.sp.playlist(playlistid)
        self.logger.info(json.dumps(playlist, indent=2))
        # print(json.dumps(playlist))

    def get_album(self, album):
        #album = self.sp.album(album)
        album = self.sp.album(album, market='ES')
        text = f"Artist: {json.dumps(album['artists'][0]['name'], indent=2)}\n"
        text = text + f"Album name: {json.dumps(album['name'], indent=2)}\n"
        text = text + f"Number tracks: {json.dumps(album['total_tracks'], indent=2)}\n"
        text = text + f"Release date: {json.dumps(album['release_date'], indent=2)}\n"
        text = text + f"Album photo: {json.dumps(album['images'][0]['url'], indent=2)}\n"
        # Itero los tracks del album
        # self.logger.info(json.dumps(album, indent=2))
        album_tracksId = []
        for track in album['tracks']['items']:
            text = text + str(track['track_number']) + " - "
            text = text + track['name'] + "\n"
            album_tracksId.append(track['id'])

        self.logger.info(text)
        self.logger.info(album_tracksId)
        return album        

    # https://open.spotify.com/playlist/0lE83xKqGubpiWolhvckBx?si=70f667133df241de
    # Obtiene las pistas de una playlist
    def get_playlistTracks(self, playlistid):
        pl_id = f'spotify:playlist:{playlistid}'
        offset = 0
        while True:
            response = self.sp.playlist_items(pl_id,
                                            offset=offset,
                                            fields='items.track.id,total',
                                            additional_types=['track'])
            # print(json.dumps(response['items']))
            if len(response['items']) == 0:
                break

            # print(response['items'])
            offset = offset + len(response['items'])
            # print(offset, "/", response['total'])
            return response['items']

    def _download(self, url):
        carpetaServidor = '/home/ubuntu/docker/python/data/src/spotify/canciones'
        spotdlcommand = f'docker run --rm -v {carpetaServidor}:/music spotdl download {url}'

        resultado = subprocess.run(['ssh', 'ubuntu@172.27.0.1', spotdlcommand])
        self.logger.info(resultado)
        # Verificar si el comando se ejecutó correctamente
        if resultado.returncode == 0:
            print("El comando se ejecutó correctamente")
        else:
            print("Se produjo un error al ejecutar el comando")

    def truncate_file(self, file):
        try:
            with open(file, "r+") as f:
                f.truncate(0)
        except FileNotFoundError:
            print('El archivo no existe')
        except:
            print('Ocurrió un error')

    def create_file_from_text(self, filename, text):
        

if __name__ == "__main__":
    playlist = "https://open.spotify.com/playlist/0lE83xKqGubpiWolhvckBx?si=06ff87b197164767"
    track =  "https://open.spotify.com/track/0sFHYyAlJL0KffCEobuftY?si=f10c9fdff90640d5"
    discovery_weekly = "https://open.spotify.com/playlist/37i9dQZEVXcTz8Pp3f26IJ?si=f2507466f7744f90"
    album = "https://open.spotify.com/album/0QedUIdHZrrX7MgHcd37WK?si=1tyq872mSw2znY9d4Ik1ug"
    

    sp = Spotify(album)
    # sp._download(track)
    # print(json.dumps(sp.get_userPlaylists("theasker")))
    # traks = sp.get_playlistTracks('0lE83xKqGubpiWolhvckBx')
    # sp.send_message( json.dumps(traks) )