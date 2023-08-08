INSERT OVERWRITE LOCAL DIRECTORY '/Users/benzhao/Documents/GitHub/Healthcare-Data-Queries/data/'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
SELECT
    REPLACE(Provider_First_Name, ',', '') AS NPI_First_Name,
    REPLACE(Provider_Last_Name_Legal_Name, ',', '') AS NPI_Last_Name,
    Provider_Middle_Name AS NPI_Middle_Initial,
    Provider_Gender_Code AS NPI_Gender_Code,
    Provider_First_Line_Business_Mailing_Address AS NPI_Address_Line_1,
    Provider_Business_Mailing_Address_City_Name AS NPI_City,
    Provider_Business_Mailing_Address_State_Name AS NPI_State,
    Provider_Business_Mailing_Address_Postal_Code AS NPI_Zip_Code
FROM hcare.NPI
