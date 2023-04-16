# scrape_metadata_only.py

from tqdm import tqdm
import os
import csv
import googleapiclient.discovery
import googleapiclient.errors


def get_video_metadata(api_key, video_id):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=api_key)

    request = youtube.videos().list(
        part="statistics",
        id=video_id
    )
    response = request.execute()

    video = response['items'][0]
    statistics = video['statistics']

    # Remove the 'favorites' field from the dictionary
    statistics.pop('favoriteCount', None)

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

    with open(output_file, 'r', newline='') as csvfile:
        existing_ids = {row['id'] for row in csv.DictReader(csvfile)}

    if metadata['id'] not in existing_ids:
        with open(output_file, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=metadata.keys())
            writer.writerow(metadata)
    else:
        print(f"Skipping duplicate video ID: {metadata['id']}")

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
    api_key = "AIzaSyA1K_PGOMvpCJmXzJ0GlOLity_ktv9ToPk"
    search_queries = [
        "Creative editing techniques",
        "Timelapse videos",
        "Stop motion animation",
        "Slow-motion videos",
        "Hyperlapse videos",
        "Video art installations",
        "Rotoscoping videos",
        "Video collages",
        "Experimental video art",
        "Animated typography videos",
        "Glitch art videos",
        "Digital paintings in motion",
        "360-degree videos",
        "Augmented reality videos",
        "Visual effects breakdowns",
        "Dynamic text animations",
        "Parallax videos",
        "Kinetic typography videos",
        "Double exposure videos",
        "Morphing animations",
        "Surreal short films",
        "Short films with hidden meanings",
        "Short films with unique camera angles",
        "Short films with nonlinear storytelling",
        "Short films with clever twists",
        "Short films with unexpected endings",
        "Short films with unconventional protagonists",
        "Short films with surreal imagery",
        "Short films with striking color palettes",
        "Short films with minimalist production design",
        "Short films with experimental sound design",
        "Short films with abstract concepts",
        "Short films with thought-provoking themes",
        "Short films with complex characters",
        "Short films with unique perspectives",
        "Short films with immersive environments",
        "Short films with visually stunning cinematography",
        "Short films with impressive special effects",
        "Short films with creative use of music",
        "Short films with strong emotional impact",
        "Short films with powerful social commentary",
        "Short films with unexpected tonal shifts",
        "Short films with engaging dialogue",
        "Short films with dreamlike sequences",
        "Short films with minimalist dialogue",
        "Short films with surreal humor",
        "Short films with inventive plot devices",
        "Short films with allegorical storytelling",
        "Short films with poetic imagery"
    ]
    max_results = 100
    output_file = f"{os.getcwd()}/data/video_metadata.csv"

    for query in search_queries:
        video_ids = get_video_ids_by_search_query(api_key, query, max_results)
        print(f"Scraping metadata for search query: {query}")

        for video_id in tqdm(video_ids, unit='video'):
            try:
                metadata = get_video_metadata(api_key, video_id)
                save_metadata_to_csv(metadata, output_file)
                print(f"Video ID: {video_id}, Metadata: {metadata}")
            except Exception as e:
                print(f"Error processing metadata for video {video_id}: {e}")
