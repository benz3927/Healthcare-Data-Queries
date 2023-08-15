import pandas as pd

# Load npi_with_dob.csv
npi_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_with_dob.csv', dtype=str)

# Load pecos_with_dob.csv
pecos_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_sample.csv', dtype=str)

# Load the file with the matches you found
sorted_indices_df = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/sorted_indices_with_weighted_scores.csv')

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

# Find the true match PECOS NPIs that you did not find
unfound_true_matches = true_match_pecos_npis - matched_pecos_npis

# Create a list to store unmatched matches
unmatched_matches = []

# Iterate through the unfound true match PECOS NPIs and find corresponding rows
for pecos_npi in unfound_true_matches:
    pecos_row = pecos_with_dob[pecos_with_dob['pecos_npi'] == pecos_npi].iloc[0]
    
    # Find the corresponding npi_row
    matching_indices = pecos_with_dob[pecos_with_dob['pecos_npi'] == pecos_npi].index.tolist()
    if matching_indices:  # Check if there's a matching npi index
        npi_row_index = matching_indices[0]
        npi_row = npi_with_dob.loc[npi_row_index]
        
        # Append the unmatched match rows to the list
        unmatched_matches.append(pd.concat([pecos_row, npi_row], ignore_index=True))

# Concatenate the list of unmatched match DataFrames
unmatched_matches_df = pd.concat(unmatched_matches, ignore_index=True)

# Save the unmatched matches DataFrame as a CSV
unmatched_matches_df.to_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/unmatched_matches.csv', index=False)



# Load the unmatched matches CSV
unmatched_matches_df = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/unmatched_matches.csv', dtype=str)

# Sort the unmatched matches DataFrame by 'nppes_npi'
unmatched_matches_df.sort_values(by='nppes_npi', inplace=True)

# Load the unmatched matches CSV
unmatched_matches_df = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/unmatched_matches.csv', dtype=str)

# Sort the unmatched matches DataFrame by the index
unmatched_matches_df.sort_index(inplace=True)

# Create a new DataFrame to store the cleaned up format
cleaned_matches_df = pd.DataFrame(columns=unmatched_matches_df.columns)

# Iterate through each unmatched match row and format the data
for idx, row in unmatched_matches_df.iterrows():
    npi = row['NPI']
    pecos_npi = row['Unmatched_NPI']
    
    npi_row = ['NPI', row['Row Label'], npi, row['First Name'], row['Last Name'],
               row['Middle Initial'], row['Gender'], row['Address Line 1'], row['City'],
               row['State'], row['Zip Code'], row['Weighted_Score']]
    
    pecos_row = ['PECOS', row['Row Label'], pecos_npi, row['First Name'], row['Last Name'],
                 row['Middle Initial'], row['Gender'], row['Address Line 1'], row['City'],
                 row['State'], row['Zip Code'], row['Weighted_Score']]
    
    cleaned_matches_df = cleaned_matches_df.append(pd.Series(npi_row, index=cleaned_matches_df.columns), ignore_index=True)
    cleaned_matches_df = cleaned_matches_df.append(pd.Series(pecos_row, index=cleaned_matches_df.columns), ignore_index=True)

# Save the cleaned matches DataFrame as a CSV
cleaned_matches_df.to_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/cleaned_matches.csv', index=False)