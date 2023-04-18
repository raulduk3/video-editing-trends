import os
import sys
import csv
from tqdm import tqdm
from scenedetect import open_video, AdaptiveDetector, SceneManager

def sanitize_string(s):
    return s.replace('\n', '\\n').replace('\r', '\\r').replace(',', '\\,')

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

def read_input_csv(input_csv):
    with open(input_csv, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [row for row in reader]
    return rows

def write_processed_data_to_csv(row, output_csv):
    if not os.path.exists(output_csv):
        with open(output_csv, 'w') as csvfile:
            fieldnames = row.keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
    with open(output_csv, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=row.keys())
        writer.writerow(row)

def is_video_processed(video_id, output_csv):
    if os.path.exists(output_csv):
        with open(output_csv, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['id'] == video_id:
                    return True
    return False

if __name__ == "__main__":
    input_csv = f"{os.getcwd()}/data/video_metadata.csv"
    output_csv = f"{os.getcwd()}/data/processed_video_with_metadata.csv"
    video_directory = f"{os.getcwd()}/data/raw_videos/"

    input_rows = read_input_csv(input_csv)

    pbar = tqdm(input_rows)
    for row in pbar:
        video_id = row['id']
        video_file_path = os.path.join(video_directory, f"{video_id}.mp4")

        if is_video_processed(video_id, output_csv):
            pbar.write(f"Video {video_id} already processed, skipping.")
            continue

        pbar.set_description("Processing %s" % video_file_path)
        pbar.refresh()

        if os.path.exists(video_file_path):
            video_data = process_video(video_file_path)
            
            row['num_shots'] = video_data['num_shots']
            row['shot_boundaries'] = sanitize_string(str(video_data['shot_boundaries']))
            row['shot_durations'] = sanitize_string(str(video_data['shot_durations']))

            write_processed_data_to_csv(row, output_csv)

            pbar.write(f"\nFor video at {video_file_path}")
            pbar.write(f"# of shots: {video_data['num_shots']}\n")
        else:
            print(f"Video file not found: {video_file_path}")
