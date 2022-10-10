select
    INCIDENT_CATEGORY,
    COUNT(INCIDENT_CATEGORY) AS COUNT_OF_INCIDENTS

from {{ source('police_staging', 'sfpd_data_2018_to_present_external_table') }}

where LOWER(INCIDENT_CATEGORY) NOT LIKE '%other%'

group by INCIDENT_CATEGORY

order by COUNT_OF_INCIDENTS DESC

limit  20
