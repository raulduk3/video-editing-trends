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
        "Funny animal videos",
        "Cute baby videos",
        "Viral dance videos",
        "Inspirational speeches",
        "Amazing nature footage",
        "Extreme sports highlights",
        "Creative cooking tutorials",
        "Prank videos",
        "Unboxing videos",
        "Product reviews",
        "Hilarious comedy sketches",
        "Educational science experiments",
        "Travel vlogs",
        "Fitness workouts",
        "Motivational videos",
        "Artistic animation shorts",
        "Music performance clips",
        "Gaming highlights",
        "Interviews with celebrities",
        "Unusual talents and skills",
        "Funny cat videos",
        "Mind-bending optical illusions",
        "Amazing magic tricks",
        "Incredible drone footage",
        "Satisfying ASMR videos",
        "Impressive street performances",
        "Fascinating documentaries",
        "Innovative technology demos",
        "DIY home improvement tutorials",
        "Pop culture commentary",
        "Short news updates",
        "Food challenges",
        "Intriguing conspiracy theories",
        "Beautiful time-lapse videos",
        "Heartwarming charity stories",
        "Challenging puzzle videos",
        "Cool science facts",
        "Life hacks",
        "Short fashion films",
        "Unusual travel destinations",
        "Viral parkour videos",
        "Funny dog videos",
        "Creative street art",
        "Bizarre experiments",
        "Virtual reality experiences",
        "Miniature model making",
        "Sped-up construction videos",
        "Short film trailers",
        "Silly lip sync videos",
        "Short animated movies",
        "Epic movie montages",
        "Compilation videos",
        "Crazy car stunts",
        "Time travel theories",
        "Short documentaries about unique professions",
        "Experimental music videos",
        "Interesting historical facts",
        "Viral skateboard videos",
        "Hilarious bloopers",
        "Life-changing self-improvement advice",
        "Cute pet compilations",
        "Short news analysis",
        "Eerie abandoned places",
        "Spectacular firework displays",
        "Awesome robot technology",
        "Celebrity impressions",
        "Gorgeous drone shots",
        "Explorations of conspiracy theories",
        "Cool art installations",
        "Unusual fashion designs",
        "Exotic animal encounters",
        "Gripping true crime stories",
        "Amazing card tricks",
        "Hilarious pet videos",
        "Unconventional beauty tutorials",
        "Epic surfing footage",
        "Innovative architecture designs",
        "Adorable kid moments",
        "Mind-blowing sand art",
        "Tasty food recipe compilations",
        "Viral football highlights",
        "Bizarre cults and religions",
        "Short skits with social commentary",
        "Funny prank compilations",
        "Fascinating archaeological discoveries",
        "Viral roller skating videos",
        "Impressive breakdancing performances",
        "Interesting urban exploration",
        "Inspirational success stories",
        "Famous speech analysis",
        "Psychedelic art videos",
        "Short films with unique concepts",
        "Viral snowboarding footage",
        "Captivating spoken word poetry"
    ]
    max_results = 100
    output_file = f"{os.getcwd()}/data/video_metadata.csv"

    for query in tqdm(search_queries):
        video_ids = get_video_ids_by_search_query(api_key, query, max_results)
        print(f"Scraping metadata for search query: {query}")

        for video_id in tqdm(video_ids, unit='video'):
            try:
                metadata = get_video_metadata(api_key, video_id)
                save_metadata_to_csv(metadata, output_file)
                print(f"Video ID: {video_id}, Metadata: {metadata}")
            except Exception as e:
                print(f"Error processing metadata for video {video_id}: {e}")
