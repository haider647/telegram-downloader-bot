import yt_dlp
import uuid

def download_video(url, quality="hd"):

    filename = f"video_{uuid.uuid4()}.mp4"

    if quality == "sd":
        fmt = "best[height<=720]"
    else:
        fmt = "best"

    ydl_opts = {
        "outtmpl": filename,
        "format": fmt,
        "noplaylist": True,
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return filename
    except:
        return None


def download_audio(url):

    filename = f"audio_{uuid.uuid4()}.mp3"

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": filename,
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return filename
    except:
        return None