# download_videos_only.py

from tqdm import tqdm
import os
import csv
import yt_dlp
import re

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

def read_video_ids_from_csv(csv_file, output_directory):
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        all_video_ids = [row['id'] for row in reader]

    downloaded_video_files = os.listdir(output_directory)
    downloaded_video_ids = [re.match(r"(.+)\.mp4", f).group(1) for f in downloaded_video_files if f.endswith(".mp4")]

    video_ids_to_download = []
    discrepancy_video_ids = []

    for video_id in all_video_ids:
        if video_id not in downloaded_video_ids:
            video_ids_to_download.append(video_id)
        else:
            discrepancy_video_ids.append(video_id)

    print(f"Total videos in CSV: {len(all_video_ids)}")
    print(f"Downloaded videos: {len(downloaded_video_ids)}")
    print(f"Videos left to download: {len(video_ids_to_download)}")

    return video_ids_to_download

def remove_duplicates_from_csv(input_csv):
    with open(input_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        unique_video_ids = {}
        for row in reader:
            video_id = row['id']
            if video_id not in unique_video_ids:
                if all(field in row for field in reader.fieldnames):
                    unique_video_ids[video_id] = row
                else:
                    print(f"Skipping row with missing or extra fields: {row}")

    with open(input_csv, 'w', newline='') as csvfile:
        fieldnames = list(unique_video_ids.values())[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in unique_video_ids.values():
            writer.writerow(row)

    print(f"Original video count: {len(list(csv.DictReader(open(input_csv, 'r'))))}")
    print(f"Unique video count: {len(unique_video_ids)}")

if __name__ == "__main__":
    input_file = f"{os.getcwd()}/data/video_metadata.csv"
    output_directory = f"{os.getcwd()}/data/raw_videos/"

    remove_duplicates_from_csv(input_file)
    video_ids = read_video_ids_from_csv(input_file, output_directory)
    

    for video_id in tqdm(video_ids, unit="video"):
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        try:
            download_video(video_url, output_directory)
        except Exception as e:
            print(f"Error processing video {video_id}: {e}")
