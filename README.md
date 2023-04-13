# pySceneDetect-clustering-analysis

This repository contains the code and data for a project analyzing trends in short-format video editing using PySceneDetect and unsupervised deep learning techniques. The project was conducted by Richard Alvarez, a student at Kenyon College IPHS Department, as part of their coursework.

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

#TODO: ## WRITE USAGE SECTION

## Project Structure
```
project_root/
│
├── data/
│   ├── raw_videos/
│   │   ├── video1.mp4
│   │   ├── video2.mp4
│   │   └── ...
│   ├── video_metadata.csv
│   └── preprocessed_features.npy
│
├── src/
│   ├── data_collection/
│   │   ├── download_videos.py
│   │   └── scrape_metadata.py
│   ├── feature_extraction/
│   │   ├── shot_boundaries.py
│   │   └── metadata_features.py
│   ├── feature_preprocessing/
│   │   ├── normalize_features.py
│   │   └── encode_features.py
│   ├── clustering/
│   │   └── unsupervised_dnn.py
│   ├── visualization/
│   │   ├── tsne_visualization.py
│   │   └── pca_visualization.py
│   └── utils.py
│
├── notebooks/
│   └── exploratory_analysis.ipynb
│
├── results/
│   ├── visualizations/
│   │   ├── tsne_plot.png
│   │   └── pca_plot.png
│   └── clustering_results.csv
│
└── README.md
```

## Dataset

The provided dataset of short-format videos was collected from various online platforms and used for analysis in this project. The dataset is included in this repository.

## Credits

This project was conducted by Richard Alvarez as part of their coursework in the Kenyon College IPHS Department. We thank them for their contributions to this project. The project is released under the MIT License.
