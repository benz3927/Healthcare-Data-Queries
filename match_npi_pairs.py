import pandas as pd
from fuzzywuzzy import fuzz
import re
import concurrent.futures

# Read the CSV files into DataFrames
npi_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_cleaned.csv'
pecos_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_cleaned.csv'
npi_df = pd.read_csv(npi_path, dtype=str)
pecos_df = pd.read_csv(pecos_path, dtype=str)

# Define columns to compare
columns_to_compare = [
    ('npi_fname', 'pecos_fname'),
    ('npi_lname', 'pecos_lname'),
    ('npi_mname', 'pecos_mname'),
    ('npi_gender', 'pecos_gender'),
    ('npi_adr1', 'pecos_adr1'),
    ('npi_city', 'pecos_city'),
    ('npi_state', 'pecos_state'),
    ('npi_zip', 'pecos_zip')
]

# Clean and preprocess values
def clean_value(value):
    return re.sub(r'[^\w\s]', '', value)

# Calculate similarity score for a pair of rows
def calculate_similarity_score(pair):
    pecos_idx, pecos_row = pair
    max_similarity_score = 0
    best_candidate_idx = None
    for npi_idx, npi_row in npi_df.iterrows():
        similarity_score = 0
        for col_pecos, col_npi in columns_to_compare:
            value1 = clean_value(str(pecos_row[col_pecos])) if not pd.isnull(pecos_row[col_pecos]) else ''
            value2 = clean_value(str(npi_row[col_npi])) if not pd.isnull(npi_row[col_npi]) else ''
            score = fuzz.token_sort_ratio(value1, value2) / 100
            similarity_score += score
        if similarity_score > max_similarity_score:
            max_similarity_score = similarity_score
            best_candidate_idx = npi_idx
    return pecos_idx, best_candidate_idx, max_similarity_score

# Create a list of pairs for parallel processing
pairs = [(pecos_idx, pecos_row) for pecos_idx, pecos_row in pecos_df.iterrows()]

# Calculate similarity scores using parallel processing
best_candidates = {}
with concurrent.futures.ProcessPoolExecutor() as executor:
    results = executor.map(calculate_similarity_score, pairs)
    for pecos_idx, npi_idx, score in results:
        if pecos_idx not in best_candidates:
            best_candidates[pecos_idx] = []
        best_candidates[pecos_idx].append((npi_idx, score))

# Export the best candidates dictionary to a CSV file
output_csv_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/npi_pair_candidates.csv'
with open(output_csv_path, 'w') as f:
    f.write("PECOS row index,Best candidate NPI row index,Max Similarity Score\n")
    for pecos_idx, candidates in best_candidates.items():
        for npi_idx, score in candidates:
            f.write(f"{pecos_idx},{npi_idx},{score}\n")

print("Matching process completed. The best candidate pairs have been exported to 'npi_pair_candidates.csv'.")
