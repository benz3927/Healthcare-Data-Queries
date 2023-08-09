import pandas as pd
import numpy as np
import pyxdameraulevenshtein as dl

# Read the CSV files into DataFrames
npi_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_cleaned.csv'
pecos_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_cleaned.csv'
npi_df = pd.read_csv(npi_path)
pecos_df = pd.read_csv(pecos_path)

# Function to calculate similarity score between two strings
def calculate_similarity_score(str1, str2):
    similarity_score = 1 - dl.normalized_damerau_levenshtein_distance(str1, str2)
    return similarity_score

# List of columns to compare in pairs
columns_to_compare = [
    'fname', 'lname', 'mname', 'gender', 'adr1', 'city', 'state', 'zip'
]

# Calculate similarity matrix
similarity_matrix = np.zeros((len(npi_df), len(pecos_df)))
for i, npi_row in npi_df.iterrows():
    for j, pecos_row in pecos_df.iterrows():
        weighted_score = 0
        for col in columns_to_compare:
            npi_col = 'npi_' + col
            pecos_col = 'pecos_' + col
            similarity_score = calculate_similarity_score(str(npi_row[npi_col]), str(pecos_row[pecos_col]))
            if col == 'fname' or col == 'lname':
                weighted_score += similarity_score * 25
            elif col == 'mname':
                weighted_score += similarity_score * 10
            elif col == 'gender':
                weighted_score += similarity_score * 10
            elif col == 'adr1':
                weighted_score += similarity_score * 25
            elif col == 'city':
                weighted_score += similarity_score * 10
            elif col == 'state':
                weighted_score += similarity_score * 15
            elif col == 'zip':
                weighted_score += similarity_score * 15
        similarity_matrix[i, j] = weighted_score

# Find best matches
threshold = 80
best_matches = {}
for i in range(len(npi_df)):
    matching_indices = np.where(similarity_matrix[i] > threshold)[0]
    if len(matching_indices) > 0:
        best_match_index = matching_indices[np.argmax(similarity_matrix[i, matching_indices])]
        best_matches[i] = [best_match_index]

# Create a DataFrame with the results
result_df = pd.DataFrame.from_dict(best_matches, orient='index', columns=['Best_Match_Pecos_Row'])

# Export the results to a CSV file
output_csv_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/best_matches.csv'
result_df.to_csv(output_csv_path, index_label='npi_row_id')

print(f"New CSV file '{output_csv_path}' has been created with best matches.")
