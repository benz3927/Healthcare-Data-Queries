import pandas as pd

def retrieve_npi_values(npi_row_index, pecos_row_indices, npi_df, pecos_df):
    npi_values = []
    
    # Retrieve NPI value for the npi_row_index
    npi_row = npi_df.loc[npi_row_index]
    npi_values.append(npi_row['nppes_npi'])  # Use the correct column name
    
    # Retrieve NPI values and row indices for the pecos_row_indices
    for pecos_row_index in pecos_row_indices:
        pecos_row = pecos_df.loc[pecos_row_index]
        npi_values.append(pecos_row['pecos_npi'])  # Add other relevant PECOS columns as needed
    
    return npi_values

# Load sorted_indices_with_weighted_scores.csv
sorted_indices_df = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/final_matches.csv')

# Load npi_with_dob.csv and pecos_with_dob.csv
npi_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_with_dob.csv', dtype=str)
pecos_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_sample.csv', dtype=str)

# Initialize a counter for correct matches and incorrect matches
correct_match_count = 0
incorrect_match_count = 0

# Iterate through the sorted indices and retrieve NPI values
for row in sorted_indices_df.itertuples():
    npi_row_index = row.npi_row_index
    pecos_row_indices = eval(row.pecos_row_indices)  # Convert string list to actual list
    
    npi_values = retrieve_npi_values(npi_row_index, pecos_row_indices, npi_with_dob, pecos_with_dob)
    
    # Check if NPI values match
    npi_match = all(npi_values[0] == npi_val for npi_val in npi_values[1:])
    
    if npi_match:
        # Retrieve the NPI and PECOS rows for printing
        npi_row = npi_with_dob.loc[npi_row_index]
        pecos_rows = pecos_with_dob.loc[pecos_row_indices]
        
        # Print the matching rows
        print("Matching rows:")
        print("NPI Row:")
        print(npi_row)
        print("PECOS Rows:")
        print(pecos_rows)
        print("--------------------")
        
        correct_match_count += 1
    else:
        # Retrieve the NPI and PECOS rows for printing
        npi_row = npi_with_dob.loc[npi_row_index]
        pecos_rows = pecos_with_dob.loc[pecos_row_indices]
        
        # Print the non-matching rows
        print("Non-matching rows:")
        print("NPI Row:")
        print(npi_row)
        print("PECOS Rows:")
        print(pecos_rows)
        print("--------------------")
        
        incorrect_match_count += 1

print(f"Number of correct matches: {correct_match_count}")
print(f"Number of incorrect matches: {incorrect_match_count}")
