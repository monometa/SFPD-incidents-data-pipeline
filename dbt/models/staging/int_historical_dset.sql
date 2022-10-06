
select 
    ID,
    Date,
    Time,
    Incident_Number,
    {{ cast_hist_2_modern_cat(Incident_Category) }} as Incident_Category,
    Incident_Description,
    Police_District,
    Resolution,
    Latitude,
    Longitude

from {{ ref('stg_historical_dset') }}