
{{ config(materialized='table')}}

with
historical as (select * from {{ ref('int_historical_dset') }}
),

modern as (select * from {{ ref('stg_modern_dset') }}
),

overall as (
    select
        *,
        ROW_NUMBER() over(order by incident_datetime) as id
    from(
        select
            incident_datetime,
            incident_number,
            incident_category,
            incident_description,
            police_district,
            resolution,
            latitude,
            longitude
        from
            historical

        union all

        select
            incident_datetime,
            incident_number,
            incident_category,
            incident_description,
            police_district,
            resolution,
            latitude,
            longitude
        from
            modern
    ) as temp_t
)

select * from overall
