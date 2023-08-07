import pandas as pd
from fuzzywuzzy import fuzz

# Read the CSV files
npi_file_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/npi_weekly.csv'
pecos_file_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/pecos.csv'

# Read the CSV files with the correct column names
npi_df = pd.read_csv(npi_file_path, usecols=[
    'provider_first_name', 'provider_last_name_legal_name',
    'provider_middle_name', 'provider_gender_code',
    'provider_first_line_business_mailing_address',
    'provider_business_mailing_address_city_name',
    'provider_business_mailing_address_state_name',
    'provider_business_mailing_address_postal_code'
], dtype='string')

pecos_df = pd.read_csv(pecos_file_path, usecols=[
    'frst_nm', 'lst_nm', 'mid_nm', 'gndr',
    'adr_ln_1', 'cty', 'st', 'zip'
], dtype='string')

# Function to calculate the weighted score
def calculate_similarity_score(row1, row2):
    weighted_score = 0

    # Define the weights for each column
    weights = {
        'provider_first_name': 25,
        'provider_last_name_legal_name': 25,
        'provider_middle_name': 10,
        'provider_gender_code': 10,
        'provider_first_line_business_mailing_address': 25,
        'provider_business_mailing_address_city_name': 10,
        'provider_business_mailing_address_state_name': 15,
        'provider_business_mailing_address_postal_code': 15
    }

    for col in npi_df.columns:
        score = fuzz.token_sort_ratio(str(row1[col]), str(row2[col])) / 100
        weighted_score += score * weights[col]

    return weighted_score

# List to store matching pairs of row indices
matching_pairs = []

# Loop through each row in pecos.csv
for pecos_index, pecos_row in pecos_df.iterrows():
    max_score = 0
    matched_npi_index = None

    # Loop through each row in npi.csv and find the row with the highest score
    for npi_index, npi_row in npi_df.iterrows():
        score = calculate_similarity_score(npi_row, pecos_row)
        if score > max_score:
            max_score = score
            matched_npi_index = npi_index

    # If the highest score is above 80, store the matching pair of row indices
    if max_score > 80:
        matching_pairs.append((matched_npi_index, pecos_index))

# Print the matching pairs
print(matching_pairs)
