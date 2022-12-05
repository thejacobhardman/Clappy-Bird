import youtube_dl
import os


def yt_download(video_url):
    video_info = youtube_dl.YoutubeDL().extract_info(url=video_url, download=False)
    filename = f"{video_info['title']}"
    save_path = os.path.join(os.getcwd(), "CustomLevels", filename)

    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',

        }],
        'outtmpl': save_path
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print("Download complete... {}".format({video_info['title']}))
    print(save_path)
