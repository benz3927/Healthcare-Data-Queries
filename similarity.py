import pandas as pd
import pyxdameraulevenshtein as dl

def calculate_dissimilarity_percentage(column1, column2):
    # The dissimilarity calculation function (same as before)

# Read the CSV file into a DataFrame
df = pd.read_csv('complete.csv')

# Assuming the two columns you want to compare are named 'Column1' and 'Column2'
column1 = df['Column1']
column2 = df['Column2']

# Calculate the dissimilarity percentage
percentage = calculate_dissimilarity_percentage(column1, column2)
print(f"Dissimilarity Percentage: {percentage:.2f}")
