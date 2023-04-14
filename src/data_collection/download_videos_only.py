# download_videos_only.py

from tqdm import tqdm
import os
import csv
import yt_dlp


def download_video(video_url, output_directory):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(output_directory, '%(id)s.%(ext)s'),
        'nocheckcertificate': True,
        'quiet': True,
        'noprogress': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        return True


def read_video_ids_from_csv(csv_file):
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        video_ids = [row['id'] for row in reader]

    return video_ids


if __name__ == "__main__":
    input_file = f"{os.getcwd()}/data/video_metadata.csv"
    output_directory = f"{os.getcwd()}/data/raw_videos/"

    video_ids = read_video_ids_from_csv(input_file)

    for video_id in tqdm(video_ids, unit="video"):
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        try:
            download_video(video_url, output_directory)
        except Exception as e:
            print(f"Error processing video {video_id}: {e}")
