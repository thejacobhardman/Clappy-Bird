import youtube_dl

def yt_download(video_url):
    video_info = youtube_dl.YoutubeDL().extract_info(url = video_url,download=False)
    filename = f"{video_info['title']}.mp3"
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl':filename,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print("Download complete... {}".format(filename))


##Currently set to download this random video, as an mp3 in the current directory - this sample code can be deleted
yt_download("https://www.youtube.com/watch?v=anDMyE6bEdI")