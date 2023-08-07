import pandas as pd
from fuzzywuzzy import fuzz
import re

# Read the CSV files into DataFrames
npi_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi/npi_weekly.csv'
pecos_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos.csv'
npi_df = pd.read_csv(npi_path, dtype=str, nrows=100)
pecos_df = pd.read_csv(pecos_path, dtype=str, nrows=100)

# Define columns to compare
columns_to_compare = [
    ('provider_last_name_legal_name', 'lst_nm'),
    ('provider_middle_name', 'mid_nm'),
    ('provider_gender_code', 'gndr'),
    ('provider_first_line_business_mailing_address', 'adr_ln_1'),
    ('provider_business_mailing_address_city_name', 'cty'),
    ('provider_business_mailing_address_state_name', 'st'),
    ('provider_business_mailing_address_postal_code', 'zip')
]

# Clean and preprocess values
def clean_value(value):
    return re.sub(r'[^\w\s]', '', value)

# Calculate similarity score for a pair of rows
def calculate_similarity_score(pecos_row):
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
    return best_candidate_idx, max_similarity_score

# Create a dictionary to store the best candidate indices
best_candidates = {}

# Calculate similarity scores for each PECOS row
for pecos_idx, pecos_row in pecos_df.iterrows():
    best_candidate_idx, max_similarity_score = calculate_similarity_score(pecos_row)
    if best_candidate_idx is not None:
        best_candidates[pecos_idx] = (best_candidate_idx, max_similarity_score)

# Print the best candidate pairs (PECOS row indices and best candidate NPI row indices)
for pecos_idx, (npi_idx, score) in best_candidates.items():
    print(f"PECOS row index {pecos_idx} has the best candidate NPI row index: {npi_idx} (Similarity Score: {score:.2f})")
