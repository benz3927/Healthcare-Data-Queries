import pandas as pd

# File paths
npi_csv_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_cleaned.csv'
pecos_csv_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_cleaned.csv'
output_csv_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/all_unique_npis.csv'

# Read CSV files
npi_df = pd.read_csv(npi_csv_path)
pecos_df = pd.read_csv(pecos_csv_path)

# Extract NPIs from both dataframes
npi_list_1 = npi_df.iloc[:, 0].tolist()
npi_list_2 = pecos_df.iloc[:, 0].tolist()

# Combine NPI lists and remove duplicates
all_unique_npi_list = list(set(npi_list_1 + npi_list_2))

# Create a DataFrame for all unique NPIs
all_unique_npi_df = pd.DataFrame({'NPI': all_unique_npi_list})

# Export DataFrame to CSV
all_unique_npi_df.to_csv(output_csv_path, index=False)
