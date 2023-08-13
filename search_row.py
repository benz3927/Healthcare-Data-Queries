import pandas as pd

# Load npi_with_dob.csv
npi_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_with_dob.csv', dtype=str)

# Load pecos_with_dob.csv
pecos_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_with_dob.csv', dtype=str)

# Print the nth row of npi_with_dob
npi_row = npi_with_dob.iloc[59]  # Replace 'n' with the row index you want to print
print("npi_with_dob:")
print(npi_row)

# Print the nth row of pecos_with_dob
pecos_row = pecos_with_dob.iloc[1975911]  # Replace 'n' with the row index you want to print
print("pecos_with_dob:")
print(pecos_row)
