select
	npi,
    frst_nm  AS pecos_fname,
    lst_nm AS pecos_lname,
    mid_nm AS pecos_mname,
    gndr AS pecos_gender,
    adr_ln_1 AS pecos_adr1,
    cty AS pecos_city,
    st AS pecos_state,
    zip AS pecos_zip,
    phn_numbr as pecos_phone
FROM hcare.pecos
