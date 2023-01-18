with mcount as (
SELECT 
   provider_first_name,
   count(1) as tcount
 FROM hcare.npi
 where provider_business_mailing_address_country_code_if_outside_us = 'US'
 and entity_type_code = '1'
 and provider_gender_code = 'M'
 group by 1
 order by 2
 ),
 

 fcount as (
SELECT 
   provider_first_name,
   count(1) as tcount 
 FROM hcare.npi
 where provider_business_mailing_address_country_code_if_outside_us = 'US'
 and entity_type_code = '1'
 and provider_gender_code = 'F'
 group by 1
 order by 2
 ),
 
-- select * from mcount
-- select * from fcount

per as (
 select 
    a.provider_first_name
    ,a.tcount as mcount
    ,b.tcount as fcount
    ,a.tcount + b.tcount as totalcount
    ,round(100.0*a.tcount/(a.tcount+b.tcount),1) as malepercent
    ,round(100.0*b.tcount/(a.tcount+b.tcount),1) as femalepercent
    ,round(100.0*abs(b.tcount-a.tcount)/(a.tcount+b.tcount),1) as diffpercent
from mcount as a
join fcount as b
on a.provider_first_name=b.provider_first_name
order by 4 desc
)

select * from per
where totalcount>1000
--and diffpercent<20
order by diffpercent 
