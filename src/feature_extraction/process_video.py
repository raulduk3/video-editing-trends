import os
import numpy as np
from tqdm import tqdm
import pandas as pd
import statistics
from scenedetect import open_video, AdaptiveDetector, SceneManager

def sanitize_string(s):
    return s.replace('\n', '\\n').replace('\r', '\\r').replace(',', '\\,')

def list_to_string(data):
    return ' '.join(map(str, data))

def load_video_data(csv_file):
    return pd.read_csv(csv_file, encoding='utf-8')

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

def get_video_features(video_path):
    shot_boundaries, shot_durations, num_shots, fps, total_frames = get_shot_boundaries_and_durations(video_path)
    shot_length_variance = statistics.variance(shot_durations) if len(shot_boundaries) > 1 else 0

    features = {
        'total_frames': total_frames,
        'shot_durations': list_to_string(shot_durations if len(shot_boundaries) > 1 else ''),
        'num_shots': num_shots,
        'shot_duration_variance': shot_length_variance,
        'average_shot_duration': round(np.mean(shot_durations), 4) if len(shot_boundaries) > 1 else 0,
    }

    return features

def process_videos(csv_file, output_csv):
    video_data = load_video_data(csv_file)

    video_features_list = []
    bar = tqdm(enumerate(video_data.iterrows()), total=len(video_data), unit="videos")
    for index, (_, video) in bar:
        bar.refresh()
        bar.set_description(f"Processing ${video['id']}")
        video_id = video['id']
        video_path = f"/Volumes/ASHCHILD I/IPHS400_DATA/{video_id}.mp4"
        features = get_video_features(video_path)

        video_features = {
            'id': video_id,
            'title': sanitize_string(str(video['title'])),
            'description': sanitize_string(str(video['description'])),
            'viewCount': int(video['viewCount']),
            'likeCount': int(video['likeCount']),
            'commentCount': int(video['commentCount']),
            'duration': float(video['duration']),
        }
        video_features.update(features)
        video_features_list.append(video_features)

        # Write video features to output CSV
        video_features_df = pd.DataFrame(video_features_list)
        video_features_df.to_csv(output_csv, index=False, encoding='utf-8')

    df = pd.read_csv(output_csv)
    print(df.head())

# Implement a function to calculate average hue, saturation, and lightness
csv_file = f'{os.getcwd()}/data/video_metadata.csv'
output_csv = f'{os.getcwd()}/data/video_features.csv'
process_videos(csv_file, output_csv)
df = pd.read_csv(output_csv)
print(df.head())
