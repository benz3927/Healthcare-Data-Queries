SELECT
    Provider_First_Name AS npi_fname,
    Provider_Last_Name_Legal_Name AS npi_lname,
    Provider_Middle_Name AS npi_mname,
    Provider_Gender_Code AS npi_gender,
    Provider_First_Line_Business_Mailing_Address AS npi_adr1,
    Provider_Business_Mailing_Address_City_Name AS npi_city,
    Provider_Business_Mailing_Address_State_Name AS NPI_State,
    Provider_Business_Mailing_Address_Postal_Code AS npi_zip
FROM hcare.NPI
