import pandas as pd
import pyxdameraulevenshtein as dl

# Load npi_with_dob.csv
npi_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_with_dob.csv', dtype=str)

# Load pecos_with_dob.csv
pecos_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_sample.csv', dtype=str)

# Load the file with the matches you found
sorted_indices_df = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/sorted_indices_with_weighted_scores.csv')

# Define the list of columns to compare
columns_to_compare = ['fname', 'lname', 'mname', 'gender', 'adr1', 'city', 'state', 'zip', 'dob', 'phone']

# Function to calculate similarity score between two strings
def calculate_similarity_score(str1, str2, column_name):
    similarity_score = 1 - dl.normalized_damerau_levenshtein_distance(str1, str2)
    return similarity_score

# Create a set to store the true match PECOS NPIs
true_match_pecos_npis = set(pecos_with_dob['pecos_npi'])

# Create a set to store the matched PECOS NPIs from your analysis
matched_pecos_npis = set()

# Fill the matched_pecos_npis set with the matched PECOS NPIs from the sorted_indices_df
for row in sorted_indices_df.itertuples():
    pecos_indices = row.pecos_row_indices.replace('[', '').replace(']', '').split(', ')
    pecos_indices = [int(index) for index in pecos_indices]
    for pecos_index in pecos_indices:
        matched_pecos_npis.add(pecos_with_dob.loc[pecos_index, 'pecos_npi'])

# Find the true matches (NPIs that are also present in the PECOS NPIs)
true_matches = npi_with_dob[npi_with_dob['nppes_npi'].isin(pecos_with_dob['pecos_npi'])]

# Find the true matches that you did not find
unfound_true_matches = true_matches[~true_matches['nppes_npi'].isin(matched_pecos_npis)]

# Create a DataFrame to store the formatted output
output_data = []

# Iterate through the unfound true matches
for index, row in unfound_true_matches.iterrows():
    npi_row = row
    pecos_row = pecos_with_dob[pecos_with_dob['pecos_npi'] == row['nppes_npi']].iloc[0]
    
    # Calculate weighted score
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
    
    # Append the formatted output for the npi row
    output_data.append(['NPI', npi_row['nppes_npi'], npi_row['npi_fname'], npi_row['npi_lname'],
                        npi_row['npi_mname'], npi_row['npi_gender'], npi_row['npi_adr1'], npi_row['npi_city'],
                        npi_row['npi_state'], npi_row['npi_zip'], weighted_score])
    
    # Append the formatted output for the pecos row
    output_data.append(['PECOS', pecos_row['pecos_npi'], pecos_row['pecos_fname'], pecos_row['pecos_lname'],
                        pecos_row['pecos_mname'], pecos_row['pecos_gender'], pecos_row['pecos_adr1'], pecos_row['pecos_city'],
                        pecos_row['pecos_state'], pecos_row['pecos_zip'], weighted_score])

# Create a DataFrame from the output_data and save it as a CSV
output_df = pd.DataFrame(output_data, columns=['Row Label', 'Matched_NPI', 'First Name', 'Last Name', 'Middle Initial',
                                               'Gender', 'Address Line 1', 'City', 'State', 'Zip Code', 'Weighted Score'])
output_df.to_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/unmatched_matches.csv', index=False)
