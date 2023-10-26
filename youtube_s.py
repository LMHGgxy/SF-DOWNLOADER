from pytube import YouTube, Search
import shutil
import logging
from os import remove
import re

logging.disable(logging.CRITICAL)

def clean_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '', filename)

def download(video_name):
    try:
        data = Search(video_name)
        url = f"https://www.youtube.com/watch?v={data.results[0].video_id}"

        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True, progressive=False).first()

        # Provide a valid output path where you want to save the downloaded file
        output_path = "C:\\Users\\luis\\Desktop\\repositorios\\SF-DOWNLOADER\\downloads\\"
        stream.download(output_path=output_path, filename=video_name)

        mp4_file_path = f"{output_path}{video_name}"
        mp3_file_path = f"{output_path}{video_name}.mp3"

        shutil.copy(mp4_file_path, mp3_file_path)
        remove(mp4_file_path)
        print(f"{video_name} descargado...")
    except:
        video_name = clean_filename(video_name)
        download(video_name)