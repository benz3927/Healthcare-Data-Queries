import pandas as pd
from fuzzywuzzy import fuzz

# Read the CSV files into DataFrames
npi_file_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/npi.csv'
pecos_file_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/pecos.csv'

npi_df = pd.read_csv(npi_file_path)
pecos_df = pd.read_csv(pecos_file_path)

# Function to calculate similarity score
def calculate_similarity_score(row1, row2):
    columns_to_compare = [
        ('provider_first_name', 'frst_nm', 25),
        ('provider_last_name_legal_name', 'lst_nm', 25),
        ('provider_middle_name', 'mid_nm', 10),
        ('provider_gender_code', 'gndr', 10),
        ('provider_first_line_business_mailing_address', 'adr_ln_1', 25),
        ('provider_business_mailing_address_city_name', 'cty', 10),
        ('provider_business_mailing_address_state_name', 'st', 15),
        ('provider_business_mailing_address_postal_code', 'zip', 15)
    ]
    similarity_score = 0
    for col1, col2, weight in columns_to_compare:
        score = fuzz.token_sort_ratio(str(row1[col1]), str(row2[col2])) / 100
        if score >= 0.8:
            similarity_score += (score * weight)
    return similarity_score

# Create a dictionary to store the matched pairs
matches = {}

# Calculate the similarity score and store the matched pairs
for npi_idx, npi_row in npi_df.iterrows():
    possible_matches = []
    for pecos_idx, pecos_row in pecos_df.iterrows():
        similarity_score = calculate_similarity_score(npi_row, pecos_row)
        if similarity_score >= 80:
            possible_matches.append(pecos_idx)
    if possible_matches:
        matches[npi_idx] = possible_matches

# Print the matched pairs (index of npi data and list of candidate indices in pecos data)
for npi_idx, pecos_indices in matches.items():
    print(f"Index {npi_idx} in NPI data matches with candidate indices: {pecos_indices}")

# Export the matches dictionary to a CSV file
output_csv_path = 'matched_pairs.csv'
pd.DataFrame.from_dict(matches, orient='index').to_csv(output_csv_path)

print("Matching process completed. The matched pairs have been exported to 'matched_pairs.csv'.")
