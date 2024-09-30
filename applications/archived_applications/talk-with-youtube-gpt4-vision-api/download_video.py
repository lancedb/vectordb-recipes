from pytube import YouTube


def download(url):
    yt_video = YouTube(url)
    yt_video = yt_video.streams.get_highest_resolution()
    yt_video.download()
    return yt_video.get_file_path()
