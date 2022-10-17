with
CY as (select * from {{ ref('stg_CY_dset') }}
),

MODERN as (select * from {{ ref('stg_modern_dset') }}
),

UNIONED as (
    select *
    from
        CY
    union all

    select *
    from
        MODERN
)

select * from UNIONED