import pandas as pd
import pyxdameraulevenshtein as dl

# Read the CSV files into DataFrames
npi_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/npi_cleaned.csv'
pecos_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/pecos_cleaned.csv'
npi_df = pd.read_csv(npi_path)
pecos_df = pd.read_csv(pecos_path)

# Function to calculate similarity score between two strings
def calculate_similarity_score(str1, str2):
    similarity_score = 1 - dl.normalized_damerau_levenshtein_distance(str1, str2)
    return similarity_score

# List of columns to compare in pairs
columns_to_compare = [
    'fname', 'lname', 'mname', 'gender', 'adr1', 'city', 'state', 'zip'
]

# Dictionary to store matched rows and their weighted scores
matched_rows = {}

# Iterate through the first 100 rows of npi and all rows of pecos
for npi_index, npi_row in npi_df.head(100).iterrows():
    npi_scores = []
    npi_address = npi_row['npi_adr1']
    for pecos_index, pecos_row in pecos_df.iterrows():
        pecos_address = pecos_row['pecos_adr1']
        address_similarity = calculate_similarity_score(npi_address, pecos_address)
        if address_similarity > 0.8:  # Change the threshold to 0.8
            weighted_score = 0
            for col in columns_to_compare:
                npi_col = 'npi_' + col
                pecos_col = 'pecos_' + col
                similarity_score = calculate_similarity_score(str(npi_row[npi_col]), str(pecos_row[pecos_col]))
                if col == 'fname' or col == 'lname':
                    weighted_score += similarity_score * 25
                elif col == 'mname':
                    weighted_score += similarity_score * 10
                elif col == 'gender':
                    weighted_score += similarity_score * 10
                elif col == 'adr1':
                    weighted_score += similarity_score * 25
                elif col == 'city':
                    weighted_score += similarity_score * 10
                elif col == 'state':
                    weighted_score += similarity_score * 15
                elif col == 'zip':
                    weighted_score += similarity_score * 15
            
            if weighted_score > 80:
                npi_scores.append((pecos_index, weighted_score))
    
    if npi_scores:
        npi_scores.sort(key=lambda x: x[1], reverse=True)
        matched_rows[npi_index] = [item[0] for item in npi_scores]

# Create a DataFrame with the results
result_df = pd.DataFrame.from_dict(matched_rows, orient='index', columns=['Possible_Matches'])

# Export the results to a CSV file
output_csv_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/possible_matches.csv'
result_df.to_csv(output_csv_path, index_label='npi_row_id')

print(f"New CSV file '{output_csv_path}' has been created with possible matches.")
