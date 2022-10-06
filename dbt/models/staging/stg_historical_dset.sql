
select 
    PdId as ID,
    FORMAT_DATE('%F', PARSE_DATE('%m/%d/%Y', Date)) AS Date,
    Time,
    IncidntNum as Incident_Number,
    INITCAP(Category) as Incident_Category,
    Descript as Incident_Description,
    INITCAP(PdDistrict) as Police_District,
    Resolution,
    Y as Latitude,
    X as Longitude

from {{ source('police_staging', 'sfpd_data_2003-to-2017_external_table') }}

where INITCAP(PdDistrict) <> 'Na' AND
    INITCAP(Category) = 'Larceny/Theft' OR
    INITCAP(Category) = 'Assault' OR
    INITCAP(Category) = 'Vehicle Theft' OR
    INITCAP(Category) = 'Drug/Narcotic' OR
    INITCAP(Category) = 'Burglary' OR
    INITCAP(Category) = 'Robbery'
