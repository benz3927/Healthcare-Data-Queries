import pandas as pd
import numpy as np

# Load npi_with_dob.csv
npi_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_with_dob.csv', dtype=str)

# Load pecos_with_dob.csv
pecos_with_dob = pd.read_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_with_dob.csv', dtype=str)

# Extract NPIs from npi_with_dob
matching_npis = npi_with_dob['nppes_npi'].tolist()

# Get matching and non-matching rows from pecos_with_dob
matching_pecos = pecos_with_dob[pecos_with_dob['pecos_npi'].isin(matching_npis)]
non_matching_pecos = pecos_with_dob[~pecos_with_dob['pecos_npi'].isin(matching_npis)]

# Sample 4000 rows of matching_pecos and 6000 rows of non_matching_pecos
matching_sample = matching_pecos.sample(n=4000, random_state=42)
non_matching_sample = non_matching_pecos.sample(n=6000, random_state=42)

# Combine the samples
pecos_sample = pd.concat([matching_sample, non_matching_sample])

# Save the combined sample to pecos_sample.csv
pecos_sample.to_csv('/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_sample.csv', index=False)

# Print the number of matching and non-matching PECOS NPIs
matching_count = matching_sample['pecos_npi'].nunique()
non_matching_count = non_matching_sample['pecos_npi'].nunique()

print(f"Final sample saved to pecos_sample.csv.")
print(f"Number of matching PECOS NPIs: {matching_count}")
print(f"Number of non-matching PECOS NPIs: {non_matching_count}")


# Extract NPIs from npi_with_dob
matching_npis = npi_with_dob['nppes_npi'].tolist()

# Get matching and non-matching rows from pecos_with_dob
matching_pecos = pecos_with_dob[pecos_with_dob['pecos_npi'].isin(matching_npis)]
non_matching_pecos = pecos_with_dob[~pecos_with_dob['pecos_npi'].isin(matching_npis)]


