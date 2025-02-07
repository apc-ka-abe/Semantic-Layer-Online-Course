{{ config(
    post_hook=[
        "OPTIMIZE ka_abe.ka_abe_dbt_silver.stg_customers;"
        ]
) }}

with

source as (

    select * from {{ source('jaffle_shop', 'jaffle_shop_customers') }}

),

renamed as (

    select

        ----------  ids
        id as customer_id,

        ---------- properties
        name

    from source

)

select * from renamed