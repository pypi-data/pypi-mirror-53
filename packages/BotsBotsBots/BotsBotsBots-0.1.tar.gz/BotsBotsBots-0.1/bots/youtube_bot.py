import os

from pytube import YouTube
from pytube import Playlist
from time import time, sleep
import ssl

import urllib.request
from bs4 import BeautifulSoup
import webbrowser

from mutagen.mp3 import MP3
from random import shuffle
# sometimes needed for youtube
ssl._create_default_https_context = ssl._create_unverified_context


# https://github.com/nficano/pytube
def download_video(url, path):
    yt = YouTube(url)
    strs = yt.streams.filter(res='1080p')
    video = strs.first()
    video.download(path)


def download_to_mp3(url, path):
    yt = YouTube(url)
    strs = yt.streams.filter(only_audio=True)
    video = strs.first()
    video.download(path)


def download_playlist(url, path):
    pl = Playlist(url)
    pl.download_all(path)


def get_yt_url(text_to_search):
    query = urllib.parse.quote(text_to_search)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    links = []
    for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
        links.append('https://www.youtube.com' + vid['href'])
    return links[0]


def open_in_browser(url):
    webbrowser.open(url)


def open_all_from_folder(folder_path):

    paths = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            paths.append(full_path)

    shuffle(paths)
    for path in paths:
        audio = MP3(path)
        name = os.path.splitext(os.path.basename(path))[0]
        open_in_browser(get_yt_url(text_to_search=name))

        length1 = audio.info.length
        print('Sleeping {} seconds: '.format(length1))
        sleep(length1)


def play(video_title):
    open_in_browser(get_yt_url(video_title))


def add_to_playlist():
    pass


if __name__ == '__main__':
    # start_time = time()
    # costel_path = 'D:/Code/Projects/Python/RLBot/videos/sample_sound.mp3'
    download_video('https://www.youtube.com/watch?v=D2sjxxoOk0I', 'E:/yt/')
    # download_playlist("https://www.youtube.com/playlist?list=PLDTu8g1oZwOqzPpzGu0AaK7hGt9H1qwF9",
    # 'D:/Code/Projects/Python/RLBot/videos')
    # download_to_mp3('https://www.youtube.com/watch?v=xwsTcSMmxlI', 'D:/Code/Projects/Python/RLBot/videos')
    # print('Finished download in {} minutes'.format((time() - start_time)/60))
    # open_in_browser('eminem venom')
    # open_all_from_folder('E:\\Music\\A')
