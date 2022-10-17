
{{ config(materialized='table') }}

with
HISTORICAL as (select * from {{ ref('int_historical') }}
),

MODERN as (select * from {{ ref('int_modern') }}
),

UNIONED as (
    select
        *,
        ROW_NUMBER() over(order by INCIDENT_DATETIME) as ID
    from(
        select
            INCIDENT_DATETIME,
            INCIDENT_NUMBER,
            INCIDENT_CATEGORY,
            INCIDENT_DESCRIPTION,
            POLICE_DISTRICT,
            RESOLUTION,
            LATITUDE,
            LONGITUDE
        from
            HISTORICAL

        union all

        select
            INCIDENT_DATETIME,
            INCIDENT_NUMBER,
            INCIDENT_CATEGORY,
            INCIDENT_DESCRIPTION,
            POLICE_DISTRICT,
            RESOLUTION,
            LATITUDE,
            LONGITUDE
        from
            MODERN
    ) as TEMP_T
)

select * from UNIONED
