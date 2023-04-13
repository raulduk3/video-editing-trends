# src/data_collection/download_and_scrape.py

import os
import csv
import yt_dlp
import googleapiclient.discovery
import googleapiclient.errors

def download_video(video_url, output_directory):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(output_directory, '%(id)s.%(ext)s'),
        'nocheckcertificate': True,
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        return True

def get_video_metadata(api_key, video_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    request = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    )
    response = request.execute()

    video = response['items'][0]
    snippet = video['snippet']
    statistics = video['statistics']

    return {
        'id': video_id,
        **statistics
    }

def save_metadata_to_csv(metadata, output_file):
    if not os.path.exists(output_file):
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = metadata.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    with open(output_file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=metadata.keys())
        writer.writerow(metadata)

def get_video_ids_by_search_query(api_key, query, max_results=50):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    request = youtube.search().list(
        part="id",
        type="video",
        q=query,
        videoDefinition="high",
        maxResults=max_results,
        fields="items(id(videoId))"
    )
    response = request.execute()

    video_ids = [item['id']['videoId'] for item in response['items']]
    return video_ids

if __name__ == "__main__":
    api_key = "AIzaSyC0VcDyYaM4zy_feKOcVhqiSGzv5ZjWdjA"
    search_query = "short videos OR reels"
    max_results = 500
    output_directory = f"{os.getcwd()}/data/raw_videos/"
    output_file = f"{os.getcwd()}/data/video_metadata.csv"

    video_ids = get_video_ids_by_search_query(api_key, search_query, max_results)

    for video_id in video_ids:
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        try:
            download_video(video_url, output_directory)
            metadata = get_video_metadata(api_key, video_id)
            save_metadata_to_csv(metadata, output_file)
            print(f"Processed video {video_id} \n {metadata} \n")
            
        except Exception as e:
            print(f"Error processing video {video_id}: {e}")
