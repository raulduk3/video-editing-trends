import os
import sys
import csv
from tqdm import tqdm
from scenedetect import open_video, AdaptiveDetector, SceneManager
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

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

def train_vectorizers(rows):
    title_vectorizer = TfidfVectorizer(max_features=100)
    desc_vectorizer = TfidfVectorizer(max_features=100)

    titles = [row['title'] for row in rows]
    descriptions = [row['description'] for row in rows]

    title_vectorizer.fit(titles)
    desc_vectorizer.fit(descriptions)

    return title_vectorizer, desc_vectorizer

def vectorize_row_text_fields(row, title_vectorizer, desc_vectorizer):
    title_vector = title_vectorizer.transform([row['title']]).toarray().flatten()
    desc_vector = desc_vectorizer.transform([row['description']]).toarray().flatten()

    row['title'] = list_to_string(title_vector)
    row['description'] = list_to_string(desc_vector)
    
def list_to_string(data):
    return ' '.join(map(str, data))

if __name__ == "__main__":
    input_csv = f"{os.getcwd()}/data/video_metadata.csv"
    output_csv = f"{os.getcwd()}/data/processed_video_with_metadata.csv"
    video_directory = f"{os.getcwd()}/data/raw_videos/"

    input_rows = read_input_csv(input_csv)
    title_vectorizer, desc_vectorizer = train_vectorizers(input_rows)

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
            row['shot_boundaries'] = list_to_string(video_data['shot_boundaries'])
            row['shot_durations'] = list_to_string(video_data['shot_durations'])

            vectorize_row_text_fields(row, title_vectorizer, desc_vectorizer)
            write_processed_data_to_csv(row, output_csv)

            pbar.write(f"\nFor video at {video_file_path}")
            pbar.write(f"# of shots: {video_data['num_shots']}\n")
        else:
            print(f"Video file not found: {video_file_path}")