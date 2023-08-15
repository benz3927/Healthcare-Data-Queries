import pandas as pd

def retrieve_npi_values(npi_row_index, pecos_row_indices, npi_df, pecos_df):
    npi_values = []
    
    # Retrieve NPI value for the npi_row_index
    npi_row = npi_df.loc[npi_row_index]
    npi_values.append(npi_row['nppes_npi'])  # Use the correct column name
    
    # Retrieve and print NPI values and row indices for the pecos_row_indices
    for pecos_row_index in pecos_row_indices:
        pecos_row = pecos_df.loc[pecos_row_index]
        npi_values.append(pecos_row['pecos_npi'])  # Add other relevant PECOS columns as needed
        print(f"Row index: NPI row index: {npi_row_index}, PECOS row index: {pecos_row_index}, NPI row NPI value: {npi_row['nppes_npi']}, PECOS row NPI value: {pecos_row['pecos_npi']}")
    
    return npi_values

# Load sorted_indices_with_weighted_scores.csv
sorted_indices_df = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/sorted_indices_with_weighted_scores.csv')

# Load npi_with_dob.csv and pecos_with_dob.csv
npi_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_with_dob.csv', dtype=str)
pecos_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_sample.csv', dtype=str)

# Iterate through the sorted indices and retrieve NPI values
for row in sorted_indices_df.itertuples():
    npi_row_index = row.npi_row_index
    pecos_row_indices = eval(row.pecos_row_indices)  # Convert string list to actual list
    
    retrieve_npi_values(npi_row_index, pecos_row_indices, npi_with_dob, pecos_with_dob)
