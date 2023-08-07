import pandas as pd
npi_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi/npi_weekly.csv'

# Read the first few lines of the CSV file
npi_df_preview = pd.read_csv(npi_path, sep='\t', nrows=10)
print(npi_df_preview)

