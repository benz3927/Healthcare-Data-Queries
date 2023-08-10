import pandas as pd

# File paths
npi_csv_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_weekly.csv'
pecos_csv_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos.csv'
output_csv_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/unique_npis.csv'

# Read CSV files
npi_df = pd.read_csv(npi_csv_path)
pecos_df = pd.read_csv(pecos_csv_path)

# Extract NPIs from both dataframes
npi_list_1 = npi_df.iloc[:, 0].tolist()
npi_list_2 = pecos_df.iloc[:, 0].tolist()

# Combine the NPI lists and get unique NPIs
unique_npi_list = list(set(npi_list_1 + npi_list_2))

# Create a DataFrame for unique NPIs
unique_npi_df = pd.DataFrame({'NPI': unique_npi_list})

# Export DataFrame to CSV
unique_npi_df.to_csv(output_csv_path, index=False)