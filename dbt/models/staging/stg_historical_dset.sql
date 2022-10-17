select
    PDID as ID,
    INCIDNTNUM as INCIDENT_NUMBER,
    DESCRIPT as INCIDENT_DESCRIPTION,
    RESOLUTION,
    Y as LATITUDE,
    X as LONGITUDE,
    DATETIME(
        PARSE_DATE('%m/%d/%Y', DATE), PARSE_TIME('%H:%M', TIME)
    ) as INCIDENT_DATETIME,
    INITCAP(CATEGORY) as INCIDENT_CATEGORY,
    INITCAP(PDDISTRICT) as POLICE_DISTRICT

from {{ source('police_staging', 'raw_historical_police_reports') }}

where INITCAP(PDDISTRICT) != 'Na'
    and INITCAP(CATEGORY) = 'Larceny/Theft' or
    INITCAP(CATEGORY) = 'Assault' or
    INITCAP(CATEGORY) = 'Vehicle Theft' or
    INITCAP(CATEGORY) = 'Drug/Narcotic' or
    INITCAP(CATEGORY) = 'Burglary' or
    INITCAP(CATEGORY) = 'Robbery'
