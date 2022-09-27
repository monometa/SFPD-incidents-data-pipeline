{{ config(materialized='table') }}


with police_data as (
    select * 
    from {{ source('staging', 'sfpd_police_data_external_table') }}
)

select 
    police_data.Incident_Datetime,
    police_data.Incident_Year,
    police_data.Report_Datetime,
    police_data.Row_ID,
    police_data.Incident_Category AS Crime,
    UPPER (police_data.Police_District) AS Police_District,
    police_data.Latitude,
    police_data.Longitude,
from police_data
    