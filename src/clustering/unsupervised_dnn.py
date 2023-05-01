# Import necessary libraries
import pandas as pd
from pycaret.classification import *
import os 

# Load the data from the CSV file
data = pd.read_csv(f"{os.getcwd()}/data/video_features.csv")

# Add a new class variable to the data
data['Class'] = pd.cut(data['viewCount'], bins=[-1, 1000, 10000, 100000, 1000000, float("inf")], labels=["Very Low", "Low", "Medium", "High", "Very High"])

# Preprocess the data to replace empty shot durations with video duration
data['shot_durations'].fillna(data['duration'], inplace=True)

# Initialize the setup
setup(data, target='Class', ignore_features = ["id"], normalize=True, fix_imbalance=True)

# Compare all models and select the best one
best_model = compare_models()

# Create the model using the best algorithm
model = create_model(best_model)

# Evaluate the model
evaluate_model(model)

# Finalize the model
final_model = finalize_model(model)

# Save the model for later use
save_model(final_model, 'final_model')
