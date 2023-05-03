# src/data_collection/download_and_scrape.py

from tqdm import tqdm
import os
import csv
import yt_dlp
import googleapiclient.discovery
import googleapiclient.errors
import isodate

def sanitize_string(s):
    return s.replace('\n', '\\n').replace('\r', '\\r').replace(',', '\\,')

def download_video(video_id, output_directory):
    video_url = f"https://www.youtube.com/watch?v={video_id}"

    ydl_opts = {
        'format': 'mp4',
        'outtmpl': os.path.join(output_directory, '%(id)s.mp4'),
        'nocheckcertificate': True,
        'quiet': True,
        'noprogress': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        return True


def get_video_metadata(api_key, video_ids):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    request = youtube.videos().list(
        part="snippet,statistics,contentDetails",
        id=",".join(video_ids)
    )
    response = request.execute()

    metadata = []
    for video in response['items']:
        snippet = video['snippet']
        statistics = video['statistics']
        content_details = video['contentDetails']

        # Remove the 'favorites' field from the dictionary
        statistics.pop('favoriteCount', None)

        duration = isodate.parse_duration(content_details['duration']).total_seconds()

        metadata.append({
            'id': video['id'],
            'title': sanitize_string(snippet['title']),
            'description': sanitize_string(snippet['description']),
            'view_count': int(statistics.get('viewCount', 0)),
            'like_count': int(statistics.get('likeCount', 0)),
            'dislike_count': int(statistics.get('dislikeCount', 0)),
            'duration': duration,
        })

    return metadata


def save_metadata_to_csv(metadata, output_file):
    if not os.path.exists(output_file):
        with open(output_file, 'w', newline='') as csvfile:
            fieldnames = metadata.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    with open(output_file, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=metadata.keys())
        writer.writerow(metadata)


def get_videos_by_search_query(api_key, query, max_results=50):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    # Step 1: Search for videos and get their IDs
    request = youtube.search().list(
        part="id",
        type="video",
        q=query,
        videoDefinition="high",
        videoDuration="short",
        maxResults=max_results,
        fields="items(id(videoId))"
    )
    response = request.execute()
    video_ids = [item['id']['videoId'] for item in response['items']]

    # Step 2: Retrieve metadata for those videos using the videos().list() method
    video_metadata = []
    for i in range(0, len(video_ids), 50):
        batch_video_ids = video_ids[i:i+50]
        request = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=",".join(batch_video_ids)
        )
        response = request.execute()
        for video in response['items']:
            snippet = video['snippet']
            statistics = video['statistics']
            content_details = video['contentDetails']

            # Remove the 'favorites' field from the dictionary
            statistics.pop('favoriteCount', None)

            duration = isodate.parse_duration(content_details['duration']).total_seconds()

            video_metadata.append({
                'id': video['id'],
                'title': sanitize_string(snippet['title']),
                'description': sanitize_string(snippet['description']),
                'view_count': int(statistics.get('viewCount', 0)),
                'like_count': int(statistics.get('likeCount', 0)),
                'dislike_count': int(statistics.get('dislikeCount', 0)),
                'duration': duration,
            })

    return video_metadata


def is_video_already_downloaded(video_id, output_directory, output_file):
    video_file = os.path.join(output_directory, f"{video_id}.mp4")
    if os.path.exists(video_file):
        return True

    with open(output_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['id'] == video_id:
                return True
    return False

if __name__ == "__main__":
    api_key = "AIzaSyA1K_PGOMvpCJmXzJ0GlOLity_ktv9ToPk"
    search_queries = [
    "Viral horse riding videos",
    "Epic water skiing stunts",
    "Amazing paper cutting tutorials",
    "Hilarious grandma moments",
    "Incredible body painting art",
    "Heartwarming animal rescues",
    "Viral basketball trick shots",
    "Fascinating ant farm videos",
    "Epic drone racing competitions",
    "Mind-blowing sand animation",
    "Viral sports bloopers",
    "Incredible balloon art",
    "Hilarious baby videos",
    "Viral martial arts demonstrations",
    "Beautiful sunset timelapses",
    "Viral dance battles",
    "Impressive fire juggling",
    "Inspirational success stories of overcoming obstacles",
    "Viral gymnastics routines",
    "Epic mountain biking stunts",
]

    max_results = 100
    output_directory = f"/Volumes/ASHCHILD I/IPHS400_DATA/"
    output_file = f"{os.getcwd()}/data/video_metadata.csv"

    pbar = tqdm(search_queries)
    for query in pbar:
        pbar.set_description(f"Searczhing: {query}")
        video_ids = get_videos_by_search_query(api_key, query, max_results)

        videos = tqdm(video_ids)
        for metadata in videos:
            video_id = metadata['id']
            videos.set_description(f"Downloading: {video_id}")

            if not is_video_already_downloaded(video_id, output_directory, output_file) and metadata['duration'] <= 300:
                try:
                    if download_video(video_id, output_directory):
                        save_metadata_to_csv(metadata, output_file)
                except Exception as e:
                    videos.write(f"Error processing video {video_id}: {e}")
            else:
                videos.write(f"Video {video_id} already downloaded, metadata exists, or its too damn long. skipping.")
