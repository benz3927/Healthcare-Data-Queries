SELECT
    npi.NPI AS NPI,
    pecos.NPI AS Matched_NPI,
    npi.provider_first_name AS NPI_First_Name,
    pecos.frst_nm AS PECOS_First_Name,
    CASE WHEN npi.provider_first_name = pecos.frst_nm THEN 25 ELSE 0 END AS First_Name_Score,
    npi.provider_last_name_legal_name AS NPI_Last_Name,
    pecos.lst_nm AS PECOS_Last_Name,
    CASE WHEN npi.provider_last_name_legal_name = pecos.lst_nm THEN 25 ELSE 0 END AS Last_Name_Score,
    SUBSTR(npi.provider_middle_name, 1, 1) AS NPI_Middle_Initial,
    SUBSTR(pecos.mid_nm, 1, 1) AS PECOS_Middle_Initial,
    CASE WHEN SUBSTR(npi.provider_middle_name, 1, 1) = SUBSTR(pecos.mid_nm, 1, 1) THEN 10 ELSE 0 END AS Middle_Name_Score,
    npi.provider_gender_code AS NPI_Gender_Code,
    pecos.gndr AS PECOS_Gender_Code,
    CASE WHEN npi.provider_gender_code = pecos.gndr THEN 10 ELSE 0 END AS Gender_Score,
    npi.provider_first_line_business_mailing_address AS NPI_Address_Line_1,
    pecos.adr_ln_1 AS PECOS_Address_Line_1,
    CASE WHEN npi.provider_first_line_business_mailing_address = pecos.adr_ln_1 THEN 25 ELSE 0 END AS Address_Line_1_Score,
    npi.provider_business_mailing_address_city_name AS NPI_City,
    pecos.cty AS PECOS_City,
    CASE WHEN npi.provider_business_mailing_address_city_name = pecos.cty THEN 10 ELSE 0 END AS City_Score,
    npi.provider_business_practice_location_address_state_name AS NPI_State,
    pecos.st AS PECOS_State,
    CASE WHEN npi.provider_business_practice_location_address_state_name = pecos.st THEN 15 ELSE 0 END AS State_Score,
    SUBSTR(npi.provider_business_mailing_address_postal_code, 1, 5) AS NPI_Zip_Code,
    SUBSTR(pecos.zip, 1, 5) AS PECOS_Zip_Code,
    CASE WHEN SUBSTR(npi.provider_business_mailing_address_postal_code, 1, 5) = SUBSTR(pecos.zip, 1, 5) THEN 15 ELSE 0 END AS Zip_Score,
    (CASE WHEN npi.provider_first_name = pecos.frst_nm THEN 1 ELSE 0 END +
    CASE WHEN npi.provider_last_name_legal_name = pecos.lst_nm THEN 1 ELSE 0 END +
    CASE WHEN SUBSTR(npi.provider_middle_name, 1, 1) = SUBSTR(pecos.mid_nm, 1, 1) THEN 1 ELSE 0 END +
    CASE WHEN npi.provider_gender_code = pecos.gndr THEN 1 ELSE 0 END +
    CASE WHEN npi.provider_first_line_business_mailing_address = pecos.adr_ln_1 THEN 1 ELSE 0 END +
    CASE WHEN npi.provider_business_mailing_address_city_name = pecos.cty THEN 1 ELSE 0 END +
    CASE WHEN npi.provider_business_practice_location_address_state_name = pecos.st THEN 1 ELSE 0 END +
    CASE WHEN SUBSTR(npi.provider_business_mailing_address_postal_code, 1, 5) = SUBSTR(pecos.zip, 1, 5) THEN 1 ELSE 0 END) AS Similarity_Score,
    ((CASE WHEN npi.provider_first_name = pecos.frst_nm THEN 1 ELSE 0 END) * 25) +
    ((CASE WHEN npi.provider_last_name_legal_name = pecos.lst_nm THEN 1 ELSE 0 END) * 25) +
    ((CASE WHEN SUBSTR(npi.provider_middle_name, 1, 1) = SUBSTR(pecos.mid_nm, 1, 1) THEN 1 ELSE 0 END) * 10) +
    ((CASE WHEN npi.provider_gender_code = pecos.gndr THEN 1 ELSE 0 END) * 10) +
    ((CASE WHEN npi.provider_first_line_business_mailing_address = pecos.adr_ln_1 THEN 1 ELSE 0 END) * 25) +
    ((CASE WHEN npi.provider_business_mailing_address_city_name = pecos.cty THEN 1 ELSE 0 END) * 10) +
    ((CASE WHEN npi.provider_business_practice_location_address_state_name = pecos.st THEN 1 ELSE 0 END) * 15) +
    ((CASE WHEN SUBSTR(npi.provider_business_mailing_address_postal_code, 1, 5) = SUBSTR(pecos.zip, 1, 5) THEN 1 ELSE 0 END) * 15) AS Total_Score
FROM hcare.npi AS npi
JOIN hcare.pecos AS pecos ON npi.NPI = pecos.NPI;
