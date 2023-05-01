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
    if not os.path.exists(video_file):
        return False

    with open(output_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['id'] == video_id:
                return True
    return False

if __name__ == "__main__":
    api_key = "AIzaSyA1K_PGOMvpCJmXzJ0GlOLity_ktv9ToPk"
    search_queries = [
        "Cute animal videos",
        "Amazing dance performances",
        "Hilarious prank videos",
        "DIY home decor tutorials",
        "Mind-blowing science experiments",
        "Inspirational quotes",
        "Beautiful nature photography",
        "Motivational speeches",
        "Gaming tutorials",
        "Funny fails",
        "Incredible sports moments",
        "Food recipe videos",
        "Cool science inventions",
        "Viral cat videos",
        "Crazy roller coaster rides",
        "Unusual art installations",
        "Creative short films",
        "Comedy sketches",
        "Impressive parkour stunts",
        "Guitar covers",
        "Fascinating travel documentaries",
        "Short horror films",
        "Interesting conspiracy theories",
        "Cool robot technology",
        "Hilarious lip sync videos",
        "Mind-bending optical illusions",
        "Amazing magic performances",
        "Cute baby animal videos",
        "Challenging brain teasers",
        "Educational history lessons",
        "Motivational workout videos",
        "Impressive drawing tutorials",
        "Artistic animation shorts",
        "Incredible acrobatics",
        "Unusual musical instruments",
        "Short film festivals",
        "Life hacks for productivity",
        "Pop culture reviews",
        "Short news segments",
        "Silly dance videos",
        "Strange food videos",
        "Viral dog videos",
        "Short biographies of famous people",
        "Fascinating scientific theories",
        "Time-lapse city videos",
        "Heartwarming charity stories",
        "Short film trailers",
        "Epic car stunts",
        "Compilation videos of funny moments",
        "Short comedy skits",
        "Short animated movies",
        "Compilation videos of epic fails",
        "Intriguing space theories",
        "Miniature model making tutorials",
        "Short documentaries about interesting people",
        "Creative music videos",
        "Amazing nature timelapses",
        "Viral skateboard videos",
        "Hilarious blooper compilations",
        "Self-improvement advice for success",
        "Cute pet moments",
        "Short political analysis",
        "Abandoned places with eerie histories",
        "Impressive drone footage",
        "Cool robot designs",
        "Celebrity impersonations",
        "Gorgeous aerial shots",
        "Explorations of paranormal activity",
        "Short fashion films",
        "Interesting fashion design",
        "Exotic animal encounters",
        "Fascinating crime stories",
        "Amazing card tricks",
        "Hilarious pet compilations",
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
    output_directory = f"{os.getcwd()}/data/raw_videos/"
    output_file = f"{os.getcwd()}/data/video_metadata.csv"

    pbar = tqdm(search_queries)
    for query in pbar:
        pbar.set_description(f"Searching: {query}")
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
