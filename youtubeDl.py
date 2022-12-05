import youtube_dl
from os import listdir
from os.path import isfile, join
import os


def yt_download(video_url):
    video_info = youtube_dl.YoutubeDL().extract_info(url = video_url,download=False)
    #filename = f"{video_info['title']}.mp3"
    #save_path = '/'.join(os.getcwd().split('/')[:3])
    #save_path = listdir("CustomLevels")

    options={
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            
         }], 
         'outtmpl': '/'.join(os.getcwd().split('/')[:3]) + {video_info['title']},  
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print("Download complete... {}".format({video_info['title']}))