import youtube_dl
import os


def yt_download(video_url):
    video_info = youtube_dl.YoutubeDL().extract_info(url = video_url,download=False)
    save_path = os.path.join(os.getcwd(), "CustomLevels")

    options={
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192', 
         }], 
         'outtmpl': save_path + '/%(title)s.%(ext)s',
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print("Download complete... {}".format({video_info['title']}))
    print(save_path)