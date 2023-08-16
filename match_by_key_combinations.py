import pandas as pd
import pyxdameraulevenshtein as dl
import re

# Load npi_with_dob.csv
npi_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_with_dob.csv', dtype=str)

# Load pecos_with_dob.csv
pecos_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_sample.csv', dtype=str)

# Perform a cross join to generate all possible combinations
combined_data = pd.merge(npi_with_dob.assign(key=1), pecos_with_dob.assign(key=1), on='key', how='outer').drop('key', axis=1)

# Initialize a list to store the candidates
candidates = []

columns_to_compare = [
    'fname', 'lname', 'mname', 'gender', 'adr1', 'city', 'state', 'zip', 'phone', 'dob'
]

# Function to calculate similarity score
def calculate_similarity_score(str1, str2):
    similarity_score = 1 - dl.normalized_damerau_levenshtein_distance(str1, str2)
    return similarity_score

# Function to sanitize string by removing special characters
def sanitize_string(s):
    s = re.sub(r'[^a-zA-Z0-9]', '', str(s))  # Remove special characters
    return s

# Iterate through each row of the combined dataset
for index, row in combined_data.iterrows():
    npi_row = row[npi_columns]  # Extract NPI row
    pecos_row = row[pecos_columns]  # Extract PECOS row
    
    weighted_score = 0
    
    for col in columns_to_compare:
        npi_col = 'npi_' + col
        pecos_col = 'pecos_' + col
        similarity_score = calculate_similarity_score(str(npi_row[npi_col]), str(pecos_row[pecos_col]))
        
        # Adjust weights as needed
        if col in ['fname', 'lname']:
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
        elif col == 'dob':
            weighted_score += similarity_score * 35
        elif col == 'phone':
            weighted_score += similarity_score * 20  # Adjust the weight as needed
    
    if weighted_score > 80:
        candidates.append({'npi_row_index': npi_row_index, 'pecos_row_index': pecos_row_index, 'weighted_score': weighted_score})

# Create a DataFrame from the candidates list
candidates_df = pd.DataFrame(candidates)

# Sort the DataFrame based on the weighted scores
candidates_df.sort_values(by='weighted_score', ascending=False, inplace=True)

# Group and store the sorted indices in a list for each row
grouped = candidates_df.groupby('npi_row_index')['pecos_row_index'].apply(list)

# Convert the grouped indices to a new DataFrame
sorted_indices_df = grouped.reset_index(name='pecos_row_indices')

# Export the DataFrame to a CSV file
output_csv_path = '/path/to/sorted_indices_with_weighted_scores_updated.csv'
sorted_indices_df.to_csv(output_csv_path, index=False)

print(f"New CSV file '{output_csv_path}' has been created with updated sorted indices and weighted scores.")

