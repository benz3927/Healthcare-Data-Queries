import pandas as pd
npi_url = 'https://github.com/benz3927/Healthcare-Data-Queries/blob/main/data/npi/npi_weekly.csv'

# Read the first few lines of the CSV file
npi_df_preview = pd.read_csv(npi_url, sep='\t', nrows=10)
print(npi_df_preview)

