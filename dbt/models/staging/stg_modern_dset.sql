select 
    Row_ID as ID,
    FORMAT_DATE('%F', PARSE_DATE('%Y/%m/%d', Incident_Date)) AS Date,
    Incident_Time AS Time,
    Incident_Number,
    Incident_Category,
    Incident_Description,
    Police_District,
    Resolution,
    Latitude,
    Longitude

from {{ source('police_staging', 'sfpd_data_2018-to-present_external_table') }}

where Police_District <> 'Out of SF' AND
    Incident_Category = 'Larceny Theft' OR
    Incident_Category = 'Assault' OR
    Incident_Category = 'Motor Vehicle Theft' OR
    Incident_Category = 'Drug Offense' OR
    Incident_Category = 'Burglary' OR
    Incident_Category = 'Robbery'
