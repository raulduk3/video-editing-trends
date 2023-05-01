# Import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pycaret.classification import *
from tabulate import tabulate
from fpdf import FPDF
import os 

# Load the data from the CSV file
data = pd.read_csv(f"{os.getcwd()}/data/video_features.csv")

# Add a new class variable to the data
data['Class'] = pd.cut(data['viewCount'], bins=[-1, 1000, 10000, 100000, 1000000, float("inf")], labels=["Very Low", "Low", "Medium", "High", "Very High"])

# Preprocess the data to replace empty shot durations with video duration
data['shot_durations'].fillna(data['duration'], inplace=True)

# Initialize the setup
setup(data, target='Class', ignore_features = ["id", "viewCount"], normalize=True, fix_imbalance=True),

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

# Get the PCA information
pca_data = get_config('X').pca.explained_variance_ratio_

# Plot the model performance
sns.set(font_scale=1.5)
plt.figure(figsize=(10,8))
plot_confusion_matrix(model)
plt.savefig('confusion_matrix.png')
plt.close()

sns.set(font_scale=1.5)
plt.figure(figsize=(10,8))
plot_classification_report(model)
plt.savefig('classification_report.png')
plt.close()

# Generate predictions on the test data
predictions = predict_model(model)

# Generate the classification report and confusion matrix
classification_report = pd.DataFrame(classification_report(predictions['Class'], predictions['Label'], output_dict=True)).transpose()
confusion_matrix = pd.DataFrame(confusion_matrix(predictions['Class'], predictions['Label'], labels=['Low', 'Medium', 'High', 'Very High']), index=['True Low', 'True Medium', 'True High', 'True Very High'], columns=['Predicted Low', 'Predicted Medium', 'Predicted High', 'Predicted Very High'])

# Save the predictions as a CSV file
predictions.to_csv('predictions.csv', index=False)

# Create a PDF report
pdf = FPDF()

# Add a page to the PDF report
pdf.add_page()

# Add the classification report to the PDF report
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'Classification Report', ln=1)
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 10, tabulate(classification_report, headers='keys', tablefmt='pipe'), ln=1)

# Add the confusion matrix to the PDF report
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'Confusion Matrix', ln=1)
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 10, tabulate(confusion_matrix, headers='keys', tablefmt='pipe'), ln=1)

# Add the PCA information to the PDF report
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'PCA Information', ln=1)
pdf.set_font('Arial', '', 12)
for i, explained_variance_ratio in enumerate(pca_data):
    pdf.cell(0, 10, f'PCA {i+1}: {explained_variance_ratio:.4f}')
    pdf.ln()

# Add the confusion matrix plot
pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'Confusion Matrix Plot', ln=1)
pdf.image('confusion_matrix.png', w=150, h=150)
pdf.ln()

pdf.set_font('Arial', 'B', 16)
pdf.cell(0, 10, 'Classification Report Plot', ln=1)
pdf.image('classification_report.png', w=150, h=150)
pdf.ln()

pdf.output('report.pdf', 'F')