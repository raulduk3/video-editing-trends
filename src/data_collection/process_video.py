# src/data_processing/process_videos.py

import os
import pandas as pd
from scenedetect import open_video, ContentDetector, SceneManager

def process_video(file_path):
    # Create a VideoManager and SceneManager
    video = open_video(file_path)
    scene_manager = SceneManager()

    # Add a ContentDetector to the SceneManager
    scene_manager.add_detector(ContentDetector())

    scene_manager.detect_scenes(video)

    # Get scene boundaries
    scene_boundaries = scene_manager.get_scene_list()

    # Calculate the number of shots
    num_shots = 1 if len(scene_boundaries) == 0 else len(scene_boundaries) 

    # Calculate shot durations
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
    csv_file = f"{os.getcwd()}/data/video_metadata.csv"
    video_directory = f"{os.getcwd()}/data/raw_videos/"

    # Read the CSV file using pandas
    df = pd.read_csv(csv_file)

    # Process each video
    for _, row in df.iterrows():
        video_id = row['id']
        video_file_path = os.path.join(video_directory, f"{video_id}.mp4")

        if os.path.exists(video_file_path):
            video_data = process_video(video_file_path)
            print(f"For video at {video_file_path}")

            # Update the corresponding row in the DataFrame
            print(f"# of shots: {video_data['num_shots']}")
            print(f"sbd: {str(video_data['shot_boundaries'])}")
            print(f"shot durations: {str(video_data['shot_durations'])}")

        else:
            print(f"Video file not found: {video_file_path}")

    # Save the updated DataFrame to the CSV file
    # df.to_csv(csv_file, index=False)

