# verify_video_files.py

import os
import csv
import re
import collections

def read_video_ids_from_csv(csv_file):
    with open(csv_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        video_ids = [row['id'] for row in reader]
    return video_ids

def get_downloaded_video_ids(directory):
    video_files = os.listdir(directory)
    video_ids = [re.match(r"(.+)\.mp4", f).group(1) for f in video_files if f.endswith(".mp4")]
    return video_ids

def delete_duplicate_files(directory, video_ids):
    duplicate_video_ids = [item for item, count in collections.Counter(video_ids).items() if count > 1]

    for video_id in duplicate_video_ids:
        duplicate_files = [file for file in os.listdir(directory) if file.startswith(video_id)]
        duplicate_files = sorted(duplicate_files)[1:]  # Keep the first file, delete the rest

        for duplicate_file in duplicate_files:
            file_path = os.path.join(directory, duplicate_file)
            os.remove(file_path)
            print(f"Deleted duplicate file: {file_path}")

if __name__ == "__main__":
    csv_file = f"{os.getcwd()}/data/video_metadata.csv"
    video_directory = f"{os.getcwd()}/data/raw_videos/"    

    csv_video_ids = read_video_ids_from_csv(csv_file)
    downloaded_video_ids = get_downloaded_video_ids(video_directory)

    missing_video_ids = set(csv_video_ids) - set(downloaded_video_ids)
    extra_video_ids = set(downloaded_video_ids) - set(csv_video_ids)

    print(f"# of missing videos: {len(missing_video_ids)}")
    print(f"# of extra videos: {len(extra_video_ids)}")

    delete_duplicate_files(video_directory, downloaded_video_ids)
