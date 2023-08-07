import pandas as pd
from fuzzywuzzy import fuzz
import re

# Read the CSV files into DataFrames
npi_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi/npi_weekly.csv'
pecos_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos.csv'
npi_df = pd.read_csv(npi_path, dtype=str)
pecos_df = pd.read_csv(pecos_path, dtype=str)

# Define columns to compare and their weights
columns_to_compare = [
    ('Provider Last Name (Legal Name)', 'lst_nm', 25),
    ('Provider Middle Name', 'mid_nm', 10),
    ('Provider Gender Code', 'gndr', 10),
    ('Provider First Line Business Mailing Address', 'adr_ln_1', 25),
    ('Provider Business Mailing Address City Name', 'cty', 10),
    ('Provider Business Mailing Address State Name', 'st', 15),
    ('Provider Business Mailing Address Postal Code', 'zip', 15)
]

# Function to preprocess and clean a value
def clean_value(value):
    # Remove special characters including commas
    cleaned_value = re.sub(r'[^\w\s]', '', value)
    return cleaned_value

# Function to calculate similarity score
def calculate_similarity_score(row1, row2):
    similarity_score = 0
    for col1, col2, weight in columns_to_compare:
        value1 = clean_value(str(row1[col1])) if not pd.isnull(row1[col1]) else ''
        value2 = clean_value(str(row2[col2])) if not pd.isnull(row2[col2]) else ''
        score = fuzz.token_sort_ratio(value1, value2) / 100
        similarity_score += (score * weight)
    return similarity_score

# Create a dictionary to store the best candidate indices
best_candidates = {}

# Calculate the similarity score for each row in pecos_df against all rows in npi_df
for pecos_idx, pecos_row in pecos_df.iterrows():
    max_similarity_score = 0
    best_candidate_idx = []
    for npi_idx, npi_row in npi_df.iterrows():
        similarity_score = calculate_similarity_score(npi_row, pecos_row)
        if similarity_score > max_similarity_score:
            max_similarity_score = similarity_score
            best_candidate_idx = [npi_idx]
        elif similarity_score == max_similarity_score:
            best_candidate_idx.append(npi_idx)
    if best_candidate_idx:
        best_candidates[pecos_idx] = best_candidate_idx

# Create a DataFrame from the best candidates dictionary
best_candidates_df = pd.DataFrame(best_candidates.items(), columns=['PECOS Row Index', 'NPI Row Index Candidates'])

# Output the best candidate pairs to the specified path
output_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/npi_pair_candidates/best_candidate_pairs.csv'
best_candidates_df.to_csv(output_path, index=False)

print("Matching process completed. The best candidate pairs have been exported to:", output_path)
