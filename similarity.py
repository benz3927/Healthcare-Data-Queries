import pandas as pd
from fuzzywuzzy import fuzz

# Read the CSV file into the DataFrame 'df'
url = 'https://raw.githubusercontent.com/benz3927/Healthcare-Data-Queries/main/data/complete.csv'
df = pd.read_csv(url)

# Function to calculate similarity score
def calculate_similarity_score(col1, col2):
    similarity_score = df.apply(lambda row: fuzz.token_sort_ratio(str(row[col1]), str(row[col2])), axis=1)
    return similarity_score/100

# List of columns to compare and add similarity scores
columns_to_compare = [
    ('NPI_First_Name', 'PECOS_First_Name'),
    ('NPI_Last_Name', 'PECOS_Last_Name'),
    ('NPI_Middle_Initial', 'PECOS_Middle_Initial'),
    ('NPI_Gender_Code', 'PECOS_Gender_Code'),
    ('NPI_Address_Line_1', 'PECOS_Address_Line_1'),
    ('NPI_City', 'PECOS_City'),
    ('NPI_State', 'PECOS_State'),
    ('NPI_Zip_Code', 'PECOS_Zip_Code')
]

# Reset the index of the DataFrame
df.reset_index(drop=True, inplace=True)

# Iterate through the list of columns to compare and calculate similarity scores
for col1, col2 in columns_to_compare:
    similarity_score = calculate_similarity_score(col1, col2)
    score_column_name = f'{col1}_String_Distance_Score'
    # Handle missing values and set the string distance score to 0
    similarity_score[df[col1].isnull() | df[col2].isnull()] = 0
    df.insert(df.columns.get_loc(col2) + 1, score_column_name, similarity_score)
    print(f"Similarity scores for columns {col1} and {col2} added as '{score_column_name}'.")

# Export the new DataFrame to a CSV file
df.to_csv('weighted_similarity_scores.csv', index=False)

# Print the new DataFrame
print(df)


# Read the CSV file into the DataFrame 'df'
url2 = 'https://raw.githubusercontent.com/benz3927/Healthcare-Data-Queries/main/weighted_similarity_scores.csv'
df = pd.read_csv(url2)

# Create a new DataFrame to store matched pairs
output_data = []
row_labels = []

for index, row in df.iterrows():
    npi_data = [
        row['NPI_First_Name'], row['NPI_Last_Name'], row['NPI_Middle_Initial'],
        row['NPI_Gender_Code'], row['NPI_Address_Line_1'], row['NPI_City'],
        row['NPI_State'], row['NPI_Zip_Code']
    ]
    
    pecos_data = [
        row['PECOS_First_Name'], row['PECOS_Last_Name'], row['PECOS_Middle_Initial'],
        row['PECOS_Gender_Code'], row['PECOS_Address_Line_1'], row['PECOS_City'],
        row['PECOS_State'], row['PECOS_Zip_Code']
    ]
    
    output_data.extend([npi_data, pecos_data])
    row_labels.extend(['NPI', 'PECOS'])

# Create a new DataFrame for the matched pairs
output_df = pd.DataFrame(output_data, columns=[
    'First Name', 'Last Name', 'Middle Initial', 'Gender',
    'Address Line 1', 'City', 'State', 'Zip Code'
])
output_df.insert(0, 'Row Label', row_labels)

# Export the new DataFrame to a CSV file
output_csv_path = '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/matched_pairs.csv'

output_df.to_csv(output_csv_path, index=False)

print("New CSV file 'matched_pairs.csv' has been created with matched pairs and alternating row labels.")
