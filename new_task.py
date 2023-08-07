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
    ('provider_last_name_legal_name', 'lst_nm', 25),
    ('provider_middle_name', 'mid_nm', 10),
    ('provider_gender_code', 'gndr', 10),
    ('provider_first_line_business_mailing_address', 'adr_ln_1', 25),
    ('provider_business_mailing_address_city_name', 'cty', 10),
    ('provider_business_mailing_address_state_name', 'st', 15),
    ('provider_business_mailing_address_postal_code', 'zip', 15)
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
    best_candidate_idx = None
    for npi_idx, npi_row in npi_df.iterrows():
        similarity_score = calculate_similarity_score(npi_row, pecos_row)
        if similarity_score > max_similarity_score:
            max_similarity_score = similarity_score
            best_candidate_idx = npi_idx
    if best_candidate_idx is not None:
        best_candidates[pecos_idx] = best_candidate_idx

# Print the best candidate pairs (PECOS row indices and best candidate NPI row indices)
for pecos_idx, npi_idx in best_candidates.items():
    print(f"PECOS row index {pecos_idx} has the best candidate NPI row index: {npi_idx}")

# Export the best candidates dictionary to a CSV file
output_csv_path = 'best_candidate_pairs.csv'
pd.DataFrame.from_dict(best_candidates, orient='index', columns=['Best_NPI_Index']).to_csv(output_csv_path)

print("Matching process completed. The best candidate pairs have been exported to 'best_candidate_pairs.csv'.")
