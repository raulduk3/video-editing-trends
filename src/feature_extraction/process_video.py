import os
import csv
import numpy as np
from tqdm import tqdm
import pandas as pd
import statistics
from scenedetect import open_video, AdaptiveDetector, SceneManager
from sklearn.feature_extraction.text import TfidfVectorizer

def get_shot_boundaries_and_durations(video_path):
    scene_manager = SceneManager()
    scene_manager.add_detector(AdaptiveDetector())
    video = open_video(video_path)
    scene_manager.detect_scenes(video)

    scene_boundaries = scene_manager.get_scene_list()
    num_shots = 1 if len(scene_boundaries) == 0 else len(scene_boundaries)

    shot_durations = [
        round((scene[1] - scene[0]).get_seconds(), 4)
        for scene in scene_boundaries
    ]
    
    fps = video.frame_rate
    total_frames = video.duration.get_frames()

    return scene_boundaries, shot_durations, num_shots, fps, total_frames

def list_to_string(data):
    return ' '.join(map(str, data))

def get_video_features(video_path):
    # clip = VideoFileClip(video_path)

    # avg_hue, avg_saturation, avg_lightness = get_average_hsl(clip, clip.fps)
    shot_boundaries, shot_durations, num_shots, fps, total_frames = get_shot_boundaries_and_durations(video_path)
    shot_length_variance = statistics.variance(shot_durations) if len(shot_boundaries) > 1 else 0
    
    features = {
        'total_frames': total_frames,
        'shot_durations': list_to_string(shot_durations if len(shot_boundaries) > 1 else ''),
        'num_shots': num_shots,
        'shot_duration_variance': shot_length_variance,
        'average_shot_duration': round(np.average(shot_durations), 4)if len(shot_boundaries) > 1 else 0,
    }

    return features

def load_video_data(csv_file):
    videos = []

    with open(csv_file, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            videos.append(row)

    return videos


def process_videos(csv_file, output_csv):
    video_data = load_video_data(csv_file)

    # Vectorize title and description
    vectorizer = TfidfVectorizer(max_features=50)
    titles = [video['title'] for video in video_data]
    descriptions = [video['description'] for video in video_data]
    title_vectors = vectorizer.fit_transform(titles).toarray()
    description_vectors = vectorizer.fit_transform(descriptions).toarray()

    # Read existing output csv file to check for already processed videos
    processed_video_ids = set()
    header_written = os.path.exists(output_csv)
    if header_written:
        with open(output_csv, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                processed_video_ids.add(row['id'])

    with open(output_csv, 'a', encoding='utf-8', newline='') as csvfile:    
        videos = tqdm(enumerate(video_data), total=len(video_data) - len(processed_video_ids), unit="videos")    
        for index, video in videos:
            video_id = video['id']

            # Skip if video has already been processed or has duration longer than 3 minutes
            if video_id in processed_video_ids or float(video['duration']) > 180:
                continue

            video_path = os.path.join('data', 'raw_videos', f"{video_id}.mp4")
            videos.set_description(f'Processing: {video_path}')
            features = get_video_features(video_path)
            video_features = {
                'id': video_id,
                'viewCount': int(video['viewCount']),
                'likeCount': int(video['likeCount']),
                'commentCount': int(video['commentCount']),
                'duration': float(video['duration']),
            }
            video_features.update(features)
            video_features.update({f'title_{i}': title_vectors[index][i] for i in range(title_vectors.shape[1])})
            video_features.update({f'description_{i}': description_vectors[index][i] for i in range(description_vectors.shape[1])})

            # Write video features to output CSV
            writer = csv.DictWriter(csvfile, fieldnames=video_features.keys())
            if not header_written:
                writer.writeheader()
                header_written = True
            writer.writerow(video_features)
            
            videos.write(f'Processesd and saved `{video_id}.mp4`.')

csv_file = '/home/ra/temp/video_metadata.csv'
output_csv = '/home/ra/temp/video_features.csv'
process_videos(csv_file, output_csv)
df = pd.read_csv(output_csv)
print(df.head())