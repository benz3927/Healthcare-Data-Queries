import pandas as pd
from fuzzywuzzy import fuzz
import re
import concurrent.futures

# Read the CSV files into DataFrames
npi_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi/npi_weekly.csv'
pecos_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos.csv'
npi_df = pd.read_csv(npi_path, dtype=str)
pecos_df = pd.read_csv(pecos_path, dtype=str)

# Define columns to compare
columns_to_compare = [
    ('Provider Last Name (Legal Name)', 'lst_nm'),
    ('Provider Middle Name', 'mid_nm'),
    ('Provider Gender Code', 'gndr'),
    ('Provider First Line Business Mailing Address', 'adr_ln_1'),
    ('Provider Business Mailing Address City Name', 'cty'),
    ('Provider Business Mailing Address State Name', 'st'),
    ('Provider Business Mailing Address Postal Code', 'zip')
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
