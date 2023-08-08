import pandas as pd

# Read the CSV files into DataFrames
npi_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi/npi_weekly.csv'
pecos_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos.csv'
npi_df = pd.read_csv(npi_path)
pecos_df = pd.read_csv(pecos_path)

# Print the 1st row in npi.csv
print("First row in npi.csv:")
print(npi_df.iloc[0])

# Print the 71st row in pecos.csv
print("71st row in pecos.csv:")
print(pecos_df.iloc[70])  # Note: Python uses 0-based indexing, so 70 corresponds to the 71st row
