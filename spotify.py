import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from os import environ
import youtube_s

load_dotenv()

reproduction_id = input("ingrese la playlist: ").split('/')[-1].split("?")[0]

client_id = environ.get('CLIENT_ID')
client_secret = environ.get('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def obtener_canciones(lista_reproduccion_id: str) -> list:
    canciones: list = []
    offset: int = 0

    while True:
        resultados = sp.playlist_items(lista_reproduccion_id, offset=offset)

        canciones += resultados['items']
        if resultados['next']:
            offset += len(resultados['items'])
        else:
            break
    canciones: list = [{'cancion': cancion['track']['name'], 'artistas':[
        artista['name'] for artista in cancion['track']['artists']]} for cancion in canciones]
    return canciones


canciones = obtener_canciones(reproduction_id)
for i in canciones:
    cancion_name = f"{i['cancion']} - {' '.join(i['artistas'])}"
    youtube_s.download(cancion_name)