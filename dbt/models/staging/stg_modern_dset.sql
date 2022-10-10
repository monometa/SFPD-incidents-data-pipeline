select
    ROW_ID as ID,
    INCIDENT_NUMBER,
    INCIDENT_CATEGORY,
    INCIDENT_DESCRIPTION,
    POLICE_DISTRICT,
    RESOLUTION,
    LATITUDE,
    LONGITUDE,
    DATETIME(INCIDENT_DATETIME) as INCIDENT_DATETIME
    
from {{ source('police_staging', 'sfpd_data_2018_to_present_external_table') }}

where POLICE_DISTRICT != 'Out of SF'
    and INCIDENT_CATEGORY = 'Larceny Theft' or
    INCIDENT_CATEGORY = 'Assault' or
    INCIDENT_CATEGORY = 'Motor Vehicle Theft' or
    INCIDENT_CATEGORY = 'Drug Offense' or
    INCIDENT_CATEGORY = 'Burglary' or
    INCIDENT_CATEGORY = 'Robbery'
