# src/data_processing/process_videos.py

import os
import sys
from tqdm import tqdm
import pandas as pd
from scenedetect import open_video, AdaptiveDetector, SceneManager

def process_video(file_path):
    video = open_video(file_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(AdaptiveDetector())

    scene_manager.detect_scenes(video)

    scene_boundaries = scene_manager.get_scene_list()
    num_shots = 1 if len(scene_boundaries) == 0 else len(scene_boundaries)

    shot_durations = [
        (scene[1] - scene[0]).get_seconds()
        for scene in scene_boundaries
    ]

    return {
        'num_shots': num_shots,
        'shot_boundaries': scene_boundaries,
        'shot_durations': shot_durations,
    }

if __name__ == "__main__":
    input_csv = f"{os.getcwd()}/data/video_metadata.csv"
    output_csv = f"{os.getcwd()}/data/video_metadata_with_scenes.csv"
    video_directory = f"{os.getcwd()}/data/raw_videos/"

    df = pd.read_csv(input_csv)

    pbar = tqdm(df.iterrows(), total=len(df.index))
    for index, row in pbar:
        video_id = row['id']
        video_file_path = os.path.join(video_directory, f"{video_id}.mp4")
        
        pbar.set_description("Processing %s" % video_file_path)
        pbar.refresh() # to show immediately the update

        if os.path.exists(video_file_path):
            video_data = process_video(video_file_path)
            
            pbar.write(f"\nFor video at {video_file_path}")

            df.at[index, 'num_shots'] = video_data['num_shots']
            df.at[index, 'shot_boundaries'] = str(video_data['shot_boundaries'])
            df.at[index, 'shot_durations'] = str(video_data['shot_durations'])

            pbar.write(f"# of shots: {video_data['num_shots']}\n")

        else:
            print(f"Video file not found: {video_file_path}")

    df.to_csv(output_csv, index=False)
