import os
import subprocess
from concurrent.futures import ThreadPoolExecutor


def download_and_extract(line):
    video_id = subprocess.check_output(['yt-dlp', '--get-id', f'http://www.youtube.com/watch?v={line}']).decode().strip()
    subprocess.call(['yt-dlp', '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo', '--no-playlist', f'http://www.youtube.com/watch?v={line}', '-o', f'./videos/{video_id}.%(ext)s'])
    os.makedirs(f'./videos/{video_id}', exist_ok=True)
    subprocess.call(['ffmpeg', '-i', f'./videos/{video_id}.mp4', '-vf', 'fps=1/30', '-vsync', '0', f'./videos/{video_id}/frame-%d.jpg'])
    os.remove(f'./videos/{video_id}.mp4')

def main(category_name):
    with open(f'category-ids/{category_name}.txt') as f:
        video_ids = f.readlines()

    num_videos = len(video_ids)
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.map(download_and_extract, video_ids[:num_videos])
if __name__ == "__main__":
    num_videos_to_download = 5
    category_to_download = "all"
    main(category_to_download)
