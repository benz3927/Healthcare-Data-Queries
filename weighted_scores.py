import pandas as pd
import pyxdameraulevenshtein as dl

# Read the CSV file into the DataFrame 'df'
path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/matched_pairs.csv'
df = pd.read_csv(path)

# List of columns to compare in pairs
columns_to_compare = [
    'First Name', 'Last Name', 'Middle Initial', 'Gender', 'Address Line 1', 'City', 'State', 'Zip Code'
]

# Function to calculate similarity score between two strings
def calculate_similarity_score(str1, str2):
    similarity_score = 1 - dl.normalized_damerau_levenshtein_distance(str1, str2)
    return similarity_score

# Calculate the weighted scores based on similarity scores
weighted_scores = []

for index, row in df.iterrows():
    if index % 2 == 1:  # PECOS row
        weighted_score_npi = 0
        weighted_score_pecos = 0
        for col in columns_to_compare:
            similarity_score = calculate_similarity_score(str(row[col]), str(df.iloc[index - 1][col]))
            if col == 'First Name' or col == 'Last Name':
                weighted_score_npi += similarity_score * 25
                weighted_score_pecos += similarity_score * 25
            elif col == 'Middle Initial':
                weighted_score_npi += similarity_score * 10
                weighted_score_pecos += similarity_score * 10
            elif col == 'Gender':
                weighted_score_npi += similarity_score * 10
                weighted_score_pecos += similarity_score * 10
            elif col == 'Address Line 1':
                weighted_score_npi += similarity_score * 25
                weighted_score_pecos += similarity_score * 25
            elif col == 'City':
                weighted_score_npi += similarity_score * 10
                weighted_score_pecos += similarity_score * 10
            elif col == 'State':
                weighted_score_npi += similarity_score * 15
                weighted_score_pecos += similarity_score * 15
            elif col == 'Zip Code':
                weighted_score_npi += similarity_score * 15
                weighted_score_pecos += similarity_score * 15
        weighted_scores.append(weighted_score_npi)
        weighted_scores.append(weighted_score_pecos)

# Add the 'Weighted_Score' column to the DataFrame
df['Weighted_Score'] = weighted_scores

# Export the new DataFrame to a CSV file
output_csv_path = 'matched_pairs_weighted_scores.csv'
df.to_csv(output_csv_path, index=False)

print(f"New CSV file '{output_csv_path}' has been created with matched pairs and weighted scores.")
