import pandas as pd

# Read the CSV file into the DataFrame 'df'
url2 = 'https://raw.githubusercontent.com/benz3927/Healthcare-Data-Queries/main/weighted_similarity_scores.csv'
df = pd.read_csv(url2)

# Check each column with "String_Distance" in its name and set the value to 0 if it's less than 0.8
for col in df.columns:
    if "String_Distance" in col:
        df[col][df[col] < 0.8] = 0

# Calculate the Weighted Score
weighted_score = (df['NPI_First_Name_String_Distance_Score'] * df['First_Name_Score']) + \
                 (df['NPI_Last_Name_String_Distance_Score'] * df['Last_Name_Score']) + \
                 (df['NPI_Middle_Initial_String_Distance_Score'] * df['Middle_Name_Score']) + \
                 (df['NPI_Gender_Code_String_Distance_Score'] * df['Gender_Score']) + \
                 (df['NPI_Address_Line_1_String_Distance_Score'] * df['Address_Line_1_Score']) + \
                 (df['NPI_City_String_Distance_Score'] * df['City_Score']) + \
                 (df['NPI_State_String_Distance_Score'] * df['State_Score']) + \
                 (df['NPI_Zip_Code_String_Distance_Score'] * df['Zip_Score'])

# Add the 'Weighted_Score' column to the DataFrame
df['Weighted_Score'] = weighted_score

# Export the new DataFrame to a CSV file
output_csv_path = 'final_weighted_scores.csv'
df.to_csv(output_csv_path, index=False)

print("New CSV file 'final_weighted_scores.csv' has been created with the additional 'Weighted_Score' column.")