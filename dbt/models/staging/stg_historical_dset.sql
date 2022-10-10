select
    PdId as ID,
    IncidntNum as Incident_Number,
    Descript as Incident_Description,
    Resolution,
    Y as Latitude,
    X as Longitude,
    DATETIME(
        PARSE_DATE('%m/%d/%Y', Date), PARSE_TIME('%H:%M', Time)
    ) as Incident_Datetime,
    INITCAP(Category) as Incident_Category,
    INITCAP(PdDistrict) as Police_District

from {{ source('police_staging', 'sfpd_data_2003_to_2017_external_table') }}

where INITCAP(PdDistrict) != 'Na'
    and INITCAP(Category) = 'Larceny/Theft' or
    INITCAP(Category) = 'Assault' or
    INITCAP(Category) = 'Vehicle Theft' or
    INITCAP(Category) = 'Drug/Narcotic' or
    INITCAP(Category) = 'Burglary' or
    INITCAP(Category) = 'Robbery'
