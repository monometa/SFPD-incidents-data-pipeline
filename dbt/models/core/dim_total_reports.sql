
{{ config(materialized='table')}}

with 
    historical as (select * from {{ ref('int_historical_dset') }}),
    modern as (select * from {{ ref('stg_modern_dset') }}),

    overall as (
        select ROW_NUMBER() OVER(ORDER BY Date) ID, *                
            FROM(
                select 
                    Date,			
                    Time,		
                    Incident_Number,				
                    Incident_Category,			
                    Incident_Description,			
                    Police_District,			
                    Resolution,			
                    Latitude    ,			
                    Longitude,
                from
                    historical

                UNION ALL 
                
                select 
                    Date,			
                    Time,		
                    Incident_Number,				
                    Incident_Category,			
                    Incident_Description,			
                    Police_District,			
                    Resolution,			
                    Latitude,			
                    Longitude,
                from
                    modern
            ) temp_t
    )

select * from overall