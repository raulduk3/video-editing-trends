# src/data_collection/download_and_scrape.py

from tqdm import tqdm
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
        'quiet': True,
        'noprogress': True
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
    search_queries = [
    "popular short videos",
    "viral tiktok compilations",
    "funny short videos",
    "viral dance videos",
    "best vines of all time",
    "most viewed youtube shorts",
    "cute animal videos",
    "short cooking videos",
    "popular movie scenes",
    "amazing trick shots",
    "viral pranks",
    "short workout videos",
    "best basketball highlights",
    "popular animated shorts",
    "short funny skits",
    "viral car videos",
    "crazy parkour videos",
    "popular music videos",
    "viral nature videos",
    "funny cat videos",
    "viral skateboard videos",
    "most watched youtube shorts",
    "short art videos",
    "viral science videos",
    "best drone videos",
    "popular gaming clips",
    "viral beauty videos",
    "funny baby videos",
    "viral roller coaster videos",
    "popular magic tricks",
    "most popular youtube shorts",
    "short travel videos",
    "viral football highlights",
    "best dance performances",
    "popular gymnastics videos",
    "funny dog videos",
    "viral skiing videos",
    "short science experiments",
    "popular slam dunk videos",
    "viral park videos",
    "best street performances",
    "popular aerial videos",
    "viral fishing videos",
    "short fashion videos",
    "viral skateboard tricks",
    "popular surfing videos",
    "funny animal videos",
    "viral roller skating videos",
    "most liked youtube shorts",
    "short documentary films",
    "viral snowboarding videos",
    "popular cycling videos",
    "best parkour videos",
    "viral escape room videos",
    "short magic shows",
    "popular acrobatics videos",
    "viral fashion shows",
    "funny prank videos",
    "viral fitness videos",
    "popular skateboarding videos",
    "short nature documentaries",
    "viral baseball highlights",
    "best comedy sketches",
    "popular aerial drone videos",
    "viral rollerblading videos",
    "short painting tutorials",
    "popular snowboarding videos",
    "viral extreme sports videos",
    "funny fail videos",
    "viral cliff jumping videos",
    "most popular youtube short films",
    "short animal documentaries",
    "viral freestyle skiing videos",
    "popular roller coaster videos",
    "best basketball trick shots",
    "viral mountain biking videos",
    "short cooking tutorials",
    "popular gymnastics performances",
    "viral magic tricks revealed",
    "funny horse videos",
    "viral fishing moments",
    "popular skiing videos",
    "best breakdance videos",
    "popular soccer highlights",
    "viral drone racing videos",
    "short movie trailers",
    "popular animal videos",
    "viral roller skating tricks",
    "funny cooking videos",
    "viral bike stunts",
    "popular breakdancing videos",
    "short sports documentaries",
    "viral escape videos",
    "best football jukes",
    "popular drone videos",
    "viral parkour fails",
    "short hair tutorials",
    "popular nature videos",
    "viral skateboard fails",
    "funny bird videos",
    "viral fishing fails",
    "popular surfing highlights",
    "best skateboarding tricks",
    "viral drone footage",
    "short meditation videos",
    "popular dance videos",
    "viral roller coaster"]
    
    max_results = 100
    output_directory = f"{os.getcwd()}/data/raw_videos/"
    output_file = f"{os.getcwd()}/data/video_metadata.csv"

    for query in search_queries:
        video_ids = get_video_ids_by_search_query(api_key, query, max_results)
        print("\033[2J")
        print(f"Downloading: {query}")

        for video_id in tqdm(video_ids, unit="video"):
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            try:
                download_video(video_url, output_directory)
                metadata = get_video_metadata(api_key, video_id)
                save_metadata_to_csv(metadata, output_file)
            except Exception as e:
                print(f"Error processing video {video_id}: {e}")
