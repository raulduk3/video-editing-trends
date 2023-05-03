# Import necessary libraries
import os
import numpy as np
import pandas as pd
import seaborn as sns
from tabulate import tabulate
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from pycaret.clustering import *

# Load the data from the CSV file
data = pd.read_csv(f"{os.getcwd()}/data/video_features.csv")

# Preprocess the data to replace empty shot durations with video duration
data['shot_durations'].fillna(data['duration'], inplace=True)

# Add a new variable "virality" based on viewCount
data['virality'] = pd.cut(data['viewCount'], bins=[-1, 1000, 10000, 100000, 1000000, float("inf")], labels=["Very Low", "Low", "Medium", "High", "Very High"])

# Initialize PyCaret setup
setup(data, normalize=True, remove_outliers=True, low_variance_threshold=0.3)

# Create the model using k-means clustering algorithm with 5 clusters
best_model = create_model("kmeans", num_clusters=5)

# Evaluate the model
evaluate_model(best_model)

# Perform Principal Component Analysis
pca = PCA(n_components=2)
principal_components = pca.fit_transform(get_config('X'))
principal_df = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
final_df = pd.concat([principal_df, data['virality']], axis=1)

# Visualize the clusters in the first two principal components
sns.scatterplot(x='PC1', y='PC2', hue='Cluster', data=get_config('X').assign(Cluster=get_config('y_km')))
plt.title('K-Means Clustering')
plt.show()

# Print the cluster labels and corresponding summary statistics for each cluster
cluster_df = pd.concat([final_df, pd.Series(get_config('y_km'), name='Cluster')], axis=1)
cluster_stats = cluster_df.groupby('Cluster').agg([np.mean, np.std])
print(tabulate(cluster_stats, headers='keys', tablefmt='psql'))
