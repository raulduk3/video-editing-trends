# Exploring Short-Format Video Editing Trends using Unsupervised Deep Learning: An AI-Powered Analysis of Creative Strategies and Technique

This repository contains the code and data for a project analyzing trends in short-format video editing using PySceneDetect and unsupervised deep learning techniques. The project was conducted by Richard Alvarez, a student at Kenyon College IPHS Department, as part of their coursework.

## Poster

![image]()

## Installation

To install the necessary Python dependencies for this project, please follow these steps:
1. Create a Python environment using [Anaconda](https://www.anaconda.com/products/individual) or [virtualenv](https://virtualenv.pypa.io/en/latest/).
2. Activate the Python environment.
3. Install the required packages using the following command:

```python
pip install -r requirements.txt
```

The required packages include PySceneDetect and other necessary dependencies.

## Usage
### Scraping Data
To scrape data from YouTube using search queries, you can use the following scripts:

download_and_scrape.py
This script downloads and scrapes videos from YouTube using search queries. It saves the video files to the data/raw_videos directory and saves the video metadata to the data/video_metadata.csv file. To run the script, use the following command:

```
python src/data_collection/download_and_scrape.py
```

verify_video_files.py
This script verifies that the video files in the data/raw_videos directory match the video metadata in the data/video_metadata.csv file. To run the script, use the following command:

```
python src/data_collection/verify_video_files.py
```

### Clustering
To cluster the data you have scraped and downlaoded, you can use the following script:

cluster.py
This script uses PyCaret to to cluster the data with specific hyperparameters. 

```
python src/clustering/cluster.py
```

### Visualization
Use the Jupyter notebooks visualize your data!

## Project Structure
```
pySceneDetect-video-editing-trends/
├── data
│   ├── extracted_features.csv
│   ├── raw_videos
│   └── video_metadata.csv
├── monitor_raw_video_folder
├── notebooks
│   └── exploratory_analysis.ipynb
├── README.md
├── requirements.txt
├── results
│   └── clustering_results.csv
└── src
    ├── clustering
    ├── data_collection
    ├── feature_extraction
    ├── feature_preprocessing
    └── visualization
```

## Dataset

The provided dataset of short-format videos was collected from various online platforms and used for analysis in this project. The dataset is included in this repository.

## Credits

This project was conducted by Richard Alvarez as part of their coursework in the Kenyon College IPHS Department. We thank them for their contributions to this project. The project is released under the MIT License.
