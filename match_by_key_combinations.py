import pandas as pd
import pyxdameraulevenshtein as dl

# Load npi_with_dob.csv
npi_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_with_dob.csv', dtype=str)

# Create the npi_key column as dob + 1st 7 characters of adr1
npi_with_dob['npi_key'] = npi_with_dob['npi_dob'].astype(str) + npi_with_dob['npi_adr1'].astype(str).str[:7]

# Load pecos_with_dob.csv
pecos_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_sample.csv', dtype=str)

# Create the pecos_key column as dob + 1st 7 characters of adr1
pecos_with_dob['pecos_key'] = pecos_with_dob['pecos_dob'].astype(str) + pecos_with_dob['pecos_adr1'].astype(str).str[:7]

# Initialize a list to store the candidates
candidates = []

# Additional key columns
npi_with_dob['key_dob_lname'] = npi_with_dob['npi_dob'].astype(str) + npi_with_dob['npi_lname'].astype(str)
npi_with_dob['key_lname_adr1'] = npi_with_dob['npi_lname'].astype(str) + npi_with_dob['npi_adr1'].astype(str).str[:7]
npi_with_dob['key_lname_phone'] = npi_with_dob['npi_lname'].astype(str) + npi_with_dob['npi_phone'].astype(str)

columns_to_compare = [
    'fname', 'lname', 'mname', 'gender', 'adr1', 'city', 'state', 'zip', 'phone', 'dob'
]

def calculate_similarity_score(str1, str2, column_name):
    similarity_score = 1 - dl.normalized_damerau_levenshtein_distance(str1, str2)
    return similarity_score

# Iterate through each row of npi_with_dob and find matching pecos indices
for npi_index, npi_row in npi_with_dob.iterrows():
    npi_keys = [npi_row['npi_key'], npi_row['key_dob_lname'], npi_row['key_lname_adr1'], npi_row['key_lname_phone']]
    
    for npi_key in npi_keys:
        pecos_indices = pecos_with_dob[pecos_with_dob['pecos_key'] == npi_key].index.tolist()
        if pecos_indices:
            for pecos_index in pecos_indices:
                candidates.append({'pecos_row_index': pecos_index, 'npi_row_index': npi_index})

# Create a DataFrame from the candidates list
candidates_df = pd.DataFrame(candidates)

# Calculate the weighted similarity scores and sort based on the scores
for candidate in candidates_df.itertuples():
    npi_row = npi_with_dob.loc[candidate.npi_row_index]
    pecos_row = pecos_with_dob.loc[candidate.pecos_row_index]
    
    weighted_score = 0
    phone_similarity_score = calculate_similarity_score(str(npi_row['npi_phone']), str(pecos_row['pecos_phone']), 'phone')
    
    for col in columns_to_compare:
        npi_col = 'npi_' + col
        pecos_col = 'pecos_' + col
        similarity_score = calculate_similarity_score(str(npi_row[npi_col]), str(pecos_row[pecos_col]), col)
        
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
        candidates_df.at[candidate.Index, 'weighted_score'] = weighted_score

# Sort the DataFrame based on the weighted scores
candidates_df.sort_values(by='weighted_score', ascending=False, inplace=True)

# Remove rows with weighted scores below 80
candidates_df = candidates_df[candidates_df['weighted_score'] > 80]

# Group and store the sorted indices in a list for each row
grouped = candidates_df.groupby('npi_row_index')['pecos_row_index'].apply(list)

# Convert the grouped indices to a new DataFrame
sorted_indices_df = grouped.reset_index(name='pecos_row_indices')

# Export the DataFrame to a CSV file
output_csv_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/sorted_indices_with_weighted_scores.csv'
sorted_indices_df.to_csv(output_csv_path, index=False)

print(f"New CSV file '{output_csv_path}' has been created with sorted indices and weighted scores.")
