import pandas as pd
from fuzzywuzzy import fuzz

# Read the CSV file into the DataFrame 'df'
url = 'https://raw.githubusercontent.com/benz3927/Healthcare-Data-Queries/main/complete.csv'
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


# 
# # Read the CSV file into the DataFrame 'df'
# url2 = 'https://raw.githubusercontent.com/benz3927/Healthcare-Data-Queries/main/weighted_similarity_scores.csv'
# df = pd.read_csv(url2)
# 
# # Calculate the Weighted Score
# weighted_score = (df['NPI_First_Name_String_Distance_Score'] * df['First_Name_Score']) + \
#                  (df['NPI_Last_Name_String_Distance_Score'] * df['Last_Name_Score']) + \
#                  (df['NPI_Middle_Initial_String_Distance_Score'] * df['Middle_Name_Score']) + \
#                  (df['NPI_Gender_Code_String_Distance_Score'] * df['Gender_Score']) + \
#                  (df['NPI_Address_Line_1_String_Distance_Score'] * df['Address_Line_1_Score']) + \
#                  (df['NPI_City_String_Distance_Score'] * df['City_Score']) + \
#                  (df['NPI_State_String_Distance_Score'] * df['State_Score']) + \
#                  (df['NPI_Zip_Code_String_Distance_Score'] * df['Zip_Score'])
# 
# # Add the 'Weighted_Score' column to the DataFrame
# df['Weighted_Score'] = weighted_score
# 
# # Export the new DataFrame to a CSV file
# output_csv_url = 'https://raw.githubusercontent.com/benz3927/Healthcare-Data-Queries/main/final_weighted_scores.csv'
# df.to_csv(output_csv_url, index=False)
# 
# print("New CSV file 'final_weighted_scores.csv' has been created with the additional 'Weighted_Score' column.")

