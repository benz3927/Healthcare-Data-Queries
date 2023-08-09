import pandas as pd
import pyxdameraulevenshtein as dl

# Load the CSV data into DataFrames
pecos_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_cleaned.csv'
npi_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_cleaned.csv'
pecos_df = pd.read_csv(pecos_path)
npi_df = pd.read_csv(npi_path)

# List of columns to compare in pairs
columns_to_compare = [
    'fname', 'lname', 'mname', 'gender', 'adr1', 'city', 'state', 'zip'
]

# Function to calculate dissimilarity percentage
def calculate_dissimilarity_percentage(column1, column2):
    total_length = len(column1)
    total_dissimilarity = 0
    for value1, value2 in zip(column1, column2):
        distance = dl.normalized_damerau_levenshtein_distance(str(value1), str(value2))
        total_dissimilarity += distance
    dissimilarity_percentage = total_dissimilarity / total_length
    return dissimilarity_percentage

# Create a DataFrame to store the results
results = []

# Match each row of the first 100 pecos with all rows of npi
for pecos_idx, pecos_row in pecos_df.head(10).iterrows():
    candidate_scores = []
    
    for npi_idx, npi_row in npi_df.iterrows():
        dissimilarity_percentage = calculate_dissimilarity_percentage(
            pecos_row[['pecos_' + col for col in columns_to_compare]],
            npi_row[['npi_' + col for col in columns_to_compare]]
        )
        
        if dissimilarity_percentage < 1:  # Adjust the threshold as needed
            candidate_scores.append((npi_idx, 1 - dissimilarity_percentage))
    
    if candidate_scores:
        candidate_scores.sort(key=lambda x: -x[1])  # Sort candidates by similarity score
        best_candidates = [str(candidate[0]) for candidate in candidate_scores]
        results.append((pecos_idx, ','.join(best_candidates)))

# Create the output CSV
output_csv_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/matched_candidates.csv'
with open(output_csv_path, 'w') as f:
    f.write("Pecos Row Index,NPI Candidate Row IDs\n")
    for pecos_idx, candidate_ids in results:
        f.write(f"{pecos_idx},{candidate_ids}\n")

print(f"Matching process completed. The results have been exported to '{output_csv_path}'.")
