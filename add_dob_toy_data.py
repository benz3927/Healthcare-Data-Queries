import pandas as pd

# Load the DOB toy data with the correct delimiter
dob_data = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/dob_toy_data.csv', delimiter='\t')

# Convert NPI values to uppercase in DOB toy data
dob_data['npi'] = dob_data['npi'].astype(str).str.upper()

# Load npi_cleaned.csv
npi_data = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_cleaned.csv')

# Merge npi_cleaned.csv with DOB data based on NPI
npi_merged = pd.merge(npi_data, dob_data[['npi', 'nppes_dob']], how='left', left_on='nppes_npi', right_on='npi')

# Rename the 'nppes_dob' column to 'npi_dob'
npi_merged.rename(columns={'nppes_dob': 'npi_dob'}, inplace=True)

# Drop the redundant 'npi' column
npi_merged.drop(columns=['npi'], inplace=True)

# Save the updated npi_cleaned.csv file
npi_merged.to_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_cleaned.csv', index=False)

# Load pecos_cleaned.csv
pecos_data = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_cleaned.csv')

# Merge pecos_cleaned.csv with DOB data based on NPI
pecos_merged = pd.merge(pecos_data, dob_data[['npi', 'pecos_dob']], how='left', left_on='pecos_npi', right_on='npi')

# Rename the 'pecos_dob' column to 'pecos_dob'
pecos_merged.rename(columns={'pecos_dob': 'pecos_dob'}, inplace=True)

# Drop the redundant 'npi' column
pecos_merged.drop(columns=['npi'], inplace=True)

# Save the updated pecos_cleaned.csv file
pecos_merged.to_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_cleaned.csv', index=False)

print("DOB data added to NPI and PECOS files.")
