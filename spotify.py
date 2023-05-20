# -*- coding: utf-8 -*-

import re
import urllib.request
import urllib.parse
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import YouTube
from dotenv import load_dotenv
from os import environ

reproduction_id = input("ingrese la playlist: ")
reproduction_id = reproduction_id.split(
    '/')[-1].split("?")[0]

load_dotenv()
client_id = environ.get('CLIENT_ID')
client_secret = environ.get('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def obtener_canciones_lista_reproduccion(lista_reproduccion_id):
    canciones = []
    offset = 0
    while True:
        resultados = sp.playlist_items(lista_reproduccion_id, offset=offset)
        canciones += resultados['items']
        if resultados['next']:
            offset += len(resultados['items'])
        else:
            break
    return canciones


canciones = obtener_canciones_lista_reproduccion(reproduction_id)

canciones_to_download = []
for cancion in canciones:
    nombre_cancion = cancion['track']['name']
    artistas = ", ".join([artista['name'] for artista in cancion['track']['artists']])
    canciones_to_download.append(f"{nombre_cancion} - {artistas}")

for cancion in canciones_to_download:
    song = cancion.replace(" ","+")
    song = urllib.parse.quote(song)
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + song)
    video_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    try:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id[0]}",)
        music_lst = yt.streams.filter(only_audio=True)
    except:
        yt = YouTube(f"https://www.youtube.com/watch?v={video_id[0]}",use_oauth=True,allow_oauth_cache=True)
        music_lst = yt.streams.filter(only_audio=True)
    cancion = cancion.replace("/","_").replace("|","_")

    music_lst[0].download(filename=f"{cancion}.mp3")
    print(f"[*] {cancion} descargado correctamente...")