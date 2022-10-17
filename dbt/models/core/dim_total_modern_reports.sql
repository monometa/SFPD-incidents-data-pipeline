select
    ID,
    INCIDENT_NUMBER,
    INCIDENT_CATEGORY,
    INCIDENT_DESCRIPTION,
    POLICE_DISTRICT,
    RESOLUTION,
    LATITUDE,
    LONGITUDE,
    INCIDENT_DATETIME

from {{ ref('int_modern') }}

where
    INCIDENT_CATEGORY in
    (select INCIDENT_CATEGORY from {{ ref('int_top20_inc_cat') }})
    and (LATITUDE is
        not null and LONGITUDE is not null)
