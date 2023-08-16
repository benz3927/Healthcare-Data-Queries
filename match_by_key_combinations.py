import pandas as pd
import pyxdameraulevenshtein as dl
import re

# Load npi_with_dob.csv
npi_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_with_dob.csv', dtype=str)

# Load pecos_with_dob.csv
pecos_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_sample.csv', dtype=str)

# Function to calculate similarity score
def calculate_similarity_score(str1, str2):
    similarity_score = 1 - dl.normalized_damerau_levenshtein_distance(str1, str2)
    return similarity_score

# Function to sanitize string by removing special characters
def sanitize_string(s):
    s = re.sub(r'[^a-zA-Z0-9]', '', str(s))  # Remove special characters
    return s

# Add key columns to NPI and PECOS DataFrames
npi_with_dob['npi_key1'] = (
    npi_with_dob['npi_dob'] + npi_with_dob['npi_adr1'].apply(sanitize_string)
)
npi_with_dob['npi_key2'] = (
    npi_with_dob['npi_dob'] + npi_with_dob['npi_lname'].apply(sanitize_string)
)
npi_with_dob['npi_key3'] = (
    npi_with_dob['npi_lname'].apply(sanitize_string) + npi_with_dob['npi_adr1'].apply(sanitize_string)
)
npi_with_dob['npi_key4'] = (
    npi_with_dob['npi_lname'].apply(sanitize_string) + npi_with_dob['npi_phone'].apply(sanitize_string)
)
npi_with_dob['npi_key5'] = (
    npi_with_dob['npi_fname'].str[:4] + npi_with_dob['npi_lname'].str[:5] + npi_with_dob['npi_dob'].apply(sanitize_string).str[:4]
)

pecos_with_dob['pecos_key1'] = (
    pecos_with_dob['pecos_dob'] + pecos_with_dob['pecos_adr1'].apply(sanitize_string)
)
pecos_with_dob['pecos_key2'] = (
    pecos_with_dob['pecos_dob'] + pecos_with_dob['pecos_lname'].apply(sanitize_string)
)
pecos_with_dob['pecos_key3'] = (
    pecos_with_dob['pecos_lname'].apply(sanitize_string) + pecos_with_dob['pecos_adr1'].apply(sanitize_string)
)
pecos_with_dob['pecos_key4'] = (
    pecos_with_dob['pecos_lname'].apply(sanitize_string) + pecos_with_dob['pecos_phone'].apply(sanitize_string)
)
pecos_with_dob['pecos_key5'] = (
    pecos_with_dob['pecos_fname'].str[:4] + pecos_with_dob['pecos_lname'].str[:5] + pecos_with_dob['pecos_dob'].apply(sanitize_string).str[:4]
)

# Initialize a list to store the candidates
candidates = []

columns_to_compare = [
    'fname', 'lname', 'mname', 'gender', 'adr1', 'city', 'state', 'zip', 'phone', 'dob'
]

# Iterate through each row of the NPI DataFrame
for npi_index, npi_row in npi_with_dob.iterrows():
    npi_keys = [npi_row['npi_key1'], npi_row['npi_key2'], npi_row['npi_key3'], npi_row['npi_key4'], npi_row['npi_key5']]
    
    matching_rows = pecos_with_dob[
        pecos_with_dob[['pecos_key1', 'pecos_key2', 'pecos_key3', 'pecos_key4', 'pecos_key5']].isin(npi_keys).any(axis=1)
    ]
    
    for pecos_index, pecos_row in matching_rows.iterrows():
        weighted_score = 0
        for col in columns_to_compare:
            npi_col = 'npi_' + col
            pecos_col = 'pecos_' + col
            similarity_score = calculate_similarity_score(str(npi_row[npi_col]), str(pecos_row[pecos_col]))
            
            if col in ['fname', 'lname']:
                weighted_score += similarity_score * 25
            if col == 'mname':
                weighted_score += similarity_score * 10
            if col == 'gender':
                weighted_score += similarity_score * 10
            if col == 'adr1':
                weighted_score += similarity_score * 25
            if col == 'city':
                weighted_score += similarity_score * 10
            if col == 'state':
                weighted_score += similarity_score * 15
            if col == 'zip':
                weighted_score += similarity_score * 15
            if col == 'dob':
                weighted_score += similarity_score * 35
            if col == 'phone':
                weighted_score += similarity_score * 20  # Adjust the weight as needed
        
        if weighted_score > 80:
            candidates.append({'npi_row_index': npi_index, 'pecos_row_index': pecos_index, 'weighted_score': weighted_score})
            
# Create a DataFrame from the candidates list
candidates_df = pd.DataFrame(candidates)

# Sort the DataFrame based on the weighted scores
candidates_df.sort_values(by='weighted_score', ascending=False, inplace=True)

# Group and store the sorted indices in a list for each NPI row
grouped = candidates_df.groupby('npi_row_index')['pecos_row_index'].apply(list)

# Convert the grouped indices to a new DataFrame
sorted_indices_df = grouped.reset_index(name='pecos_row_indices')

# Export the DataFrame to a CSV file
output_csv_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/final_matches.csv'
sorted_indices_df.to_csv(output_csv_path, index=False)

print(f"New CSV file '{output_csv_path}' has been created with updated sorted indices and weighted scores.")