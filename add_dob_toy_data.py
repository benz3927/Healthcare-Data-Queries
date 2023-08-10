import pandas as pd

# Load the DOB toy data with the correct delimiter
dob_data = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/dob_toy_data.csv', delimiter='\t')

# Split the combined column into separate columns
dob_data[['npi', 'nppes_dob', 'pecos_dob']] = dob_data['NPI,NPPES_DOB,PECOS_DOB'].str.split('\t', expand=True)

# Define the columns to check for matching NPI values
columns_to_check = ['npi', 'nppes_npi', 'pecos_npi']

# Load npi_cleaned.csv
npi_data = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_cleaned.csv')

# Load pecos_cleaned.csv
pecos_data = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_cleaned.csv')

# Iterate through the columns and merge DOB data
for column in columns_to_check:
    dob_data[column] = dob_data[column].astype(str).str.upper()  # Convert NPI values to uppercase
    npi_data = pd.merge(npi_data, dob_data[[column, 'nppes_dob']], how='left', left_on='nppes_npi', right_on=column)
    pecos_data = pd.merge(pecos_data, dob_data[[column, 'pecos_dob']], how='left', left_on='pecos_npi', right_on=column)

# Save the updated npi_cleaned.csv file
npi_data.to_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_cleaned.csv', index=False)

# Save the updated pecos_cleaned.csv file
pecos_data.to_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_cleaned.csv', index=False)

print("DOB data added to NPI and PECOS files.")
