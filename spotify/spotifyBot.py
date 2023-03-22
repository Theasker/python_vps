import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sys
sys.path.append("..")
from telegramBot.telegramBot import TelegramBot
import subprocess

class Spotify(TelegramBot):
    def __init__(self, url):
        self._inifile = '/usr/src/app/spotify/config.json'
        self._inivars = {} # Creo un diccionario para las variables del fichero
        self._get_inivars()
        # Carga el token del bot en la clase heredada
        # super().__init__(self._inivars['TELEGRAMBOTTOKEN'])
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=self._inivars['CLIENTID'], client_secret=self._inivars['CLIENTSECRET']))
        self._dispatch(url)

    def _get_inivars(self):
        try:
            with open(self._inifile, 'r') as file:
                self._inivars = json.load(file)
        except OSError:
            print("Could not open/read file:", fname)
            sys.exit()

    def _dispatch(self, url):
        if ('playlist' in 'url'):
            print('playlist')

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

            print(response['items'])
            offset = offset + len(response['items'])
            print(offset, "/", response['total'])
            return response['items']

    def _download(self, url):
        carpetaServidor = '/home/ubuntu/docker/python/data/src/spotify/canciones'
        spotdlcommand = f'docker run --rm -v {carpetaServidor}:/music spotdl download {url}'

        resultado = subprocess.run(['ssh', 'ubuntu@172.27.0.1', spotdlcommand])

        # Verificar si el comando se ejecutó correctamente
        if resultado.returncode == 0:
            print("El comando se ejecutó correctamente")
        else:
            print("Se produjo un error al ejecutar el comando")

if __name__ == "__main__":
    # https://open.spotify.com/playlist/37i9dQZF1E37e4h5zszmNm?si=1add55e9d58d4d99
    # https://open.spotify.com/track/0sFHYyAlJL0KffCEobuftY?si=f10c9fdff90640d5
    # https://open.spotify.com/playlist/37i9dQZEVXcTz8Pp3f26IJ?si=a709282848b04717

    sp = Spotify()
    # print(json.dumps(sp.get_userPlaylists("theasker")))
    traks = sp.get_playlistTracks('0lE83xKqGubpiWolhvckBx')
    # sp.send_message( json.dumps(traks) )