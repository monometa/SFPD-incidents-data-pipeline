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

where
    INCIDENT_CATEGORY in
    (select INCIDENT_CATEGORY from {{ ref('stg_top20_inc_cat') }})
    and (LATITUDE is
        not null and LONGITUDE is not null)
