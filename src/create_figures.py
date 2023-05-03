import os
import cv2
import random
import math
from moviepy.editor import VideoFileClip
from PIL import Image, ImageDraw, ImageFont

def get_thumbnail(video_path, time_stamp=1):
    clip = VideoFileClip(video_path)
    thumbnail = clip.get_frame(time_stamp)
    return cv2.cvtColor(thumbnail, cv2.COLOR_RGB2RGBA)

def create_composite_image(directory, output_path, thumbnail_size=(100, 100), padding=10, font_size=20):
    mp4_files = random.sample([file for file in os.listdir(directory) if file.endswith('.mp4')], 100)
    thumbnails = []

    for file in mp4_files:
        thumbnail = get_thumbnail(os.path.join(directory, file))
        thumbnail = cv2.resize(thumbnail, thumbnail_size)
        thumbnails.append((thumbnail, file))

    num_files = len(thumbnails)
    grid_size = math.ceil(math.sqrt(num_files))
    composite_width = (thumbnail_size[0] + padding) * grid_size + padding
    composite_height = (thumbnail_size[1] + padding + font_size) * grid_size + padding

    composite_image = Image.new('RGB', (composite_width, composite_height), 'white')
    font = ImageFont.load_default()

    x, y = padding, padding
    for thumbnail, file_name in thumbnails:
        img = Image.fromarray(thumbnail)
        composite_image.paste(img, (x, y))
        draw = ImageDraw.Draw(composite_image)
        draw.text((x, y + thumbnail_size[1]), f'ID: {file_name}', (0, 0, 0), font=font)

        x += thumbnail_size[0] + padding
        if (x + thumbnail_size[0] + padding) > composite_width:
            x = padding
            y += thumbnail_size[1] + padding + font_size

    composite_image.save(output_path)

if __name__ == "__main__":
    directory = "/Volumes/ASHCHILD I/IPHS400_DATA/"
    output_path = f"{os.getcwd()}/composite_image.jpg"
    create_composite_image(directory, output_path)
