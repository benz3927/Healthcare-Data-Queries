import pandas as pd
import pyxdameraulevenshtein as dl

# Load npi_with_dob.csv
npi_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_with_dob.csv', dtype=str)

# Create the npi_key column
npi_with_dob['npi_key'] = npi_with_dob['npi_dob'].astype(str) + npi_with_dob['npi_adr1'].astype(str).str.replace(' ', '')

# Load pecos_with_dob.csv
pecos_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_sample.csv', dtype=str)

# Create the pecos_key column
pecos_with_dob['pecos_key'] = pecos_with_dob['pecos_dob'].astype(str) + pecos_with_dob['pecos_adr1'].astype(str).str.replace(' ', '')

# Initialize a list to store the candidates
candidates = []

# Iterate through each row of npi_with_dob and find matching pecos indices
for npi_index, npi_row in npi_with_dob.iterrows():
    npi_key = npi_row['npi_key']
    matching_indices = pecos_with_dob[pecos_with_dob['pecos_key'] == npi_key].index.tolist()
    for pecos_index in matching_indices:
        candidates.append({'pecos_row_index': pecos_index, 'npi_row_index': npi_index})

# Create a DataFrame from the candidates list
candidates_df = pd.DataFrame(candidates)

# Function to calculate similarity score between two strings
def calculate_similarity_score(str1, str2, column_name):
    similarity_score = 1 - dl.normalized_damerau_levenshtein_distance(str1, str2)
    return similarity_score

# List of columns to compare in pairs
columns_to_compare = [
    'fname', 'lname', 'mname', 'gender', 'adr1', 'city', 'state', 'zip', 'dob'
]

# Initialize a dictionary to store the matching pairs
matched_pairs = {'pecos_row_index': [], 'npi_row_indices': []}

# Iterate through the candidates and calculate weighted similarity scores
for candidate in candidates_df.itertuples():
    npi_row = npi_with_dob.loc[candidate.npi_row_index]
    pecos_row = pecos_with_dob.loc[candidate.pecos_row_index]
    
    weighted_score = 0
    for col in columns_to_compare:
        npi_col = 'npi_' + col
        pecos_col = 'pecos_' + col
        similarity_score = calculate_similarity_score(str(npi_row[npi_col]), str(pecos_row[pecos_col]), col)
        
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
        elif col == 'dob':
            weighted_score += similarity_score * 35
    
    if weighted_score > 80:  # Change the threshold if needed
        matched_pairs['pecos_row_index'].append(candidate.pecos_row_index)
        matched_pairs['npi_row_indices'].append(candidate.npi_row_index)

# Create a DataFrame with the matching pairs
matched_pairs_df = pd.DataFrame(matched_pairs)

# Export the DataFrame to a CSV file
output_csv_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/matched_pairs_with_key_priority.csv'
matched_pairs_df.to_csv(output_csv_path, index=False)

print(f"New CSV file '{output_csv_path}' has been created with matched pairs and key priority.")
