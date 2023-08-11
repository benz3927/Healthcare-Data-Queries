import pandas as pd

# Load toy data
toy_data = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/dob_toy_data.csv', delimiter='\t', dtype=str)

# Split the combined column name and assign correct column names
toy_data[['NPI', 'NPPES_DOB', 'PECOS_DOB']] = toy_data['NPI,NPPES_DOB,PECOS_DOB'].str.split(',', expand=True)

# Load npi.csv
npi_data = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_cleaned.csv', dtype=str)

# Merge toy_data with npi_data based on 'NPI'
npi_merged = npi_data.merge(toy_data[['NPI', 'NPPES_DOB']], how='left', left_on='nppes_npi', right_on='NPI')

# Load pecos.csv
pecos_data = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_cleaned.csv', dtype=str)

# Merge toy_data with pecos_data based on 'NPI'
pecos_merged = pecos_data.merge(toy_data[['NPI', 'PECOS_DOB']], how='left', left_on='pecos_npi', right_on='NPI')

# Drop the extra 'NPI' columns from npi_merged and pecos_merged
npi_merged.drop(columns=['NPI'], inplace=True)
pecos_merged.drop(columns=['NPI'], inplace=True)

# Convert column names to lowercase
npi_merged.columns = npi_merged.columns.str.lower()
pecos_merged.columns = pecos_merged.columns.str.lower()

# Save the updated npi.csv and pecos.csv files
npi_merged.to_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_with_dob.csv', index=False)
pecos_merged.to_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_with_dob.csv', index=False)

print("DOB column added to npi.csv and pecos.csv.")
