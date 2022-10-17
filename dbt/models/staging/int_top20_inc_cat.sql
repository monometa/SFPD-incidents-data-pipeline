select
    INCIDENT_CATEGORY,
    COUNT(INCIDENT_CATEGORY) as COUNT_OF_INCIDENTS

from {{ ref('int_modern') }}

where LOWER(INCIDENT_CATEGORY) not like '%other%'
group by INCIDENT_CATEGORY
order by COUNT_OF_INCIDENTS desc
limit 20
