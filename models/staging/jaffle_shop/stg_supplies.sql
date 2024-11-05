{{ config(
    post_hook=[
        "OPTIMIZE ka_abe.ka_abe_dbt_silver.stg_supplies;"
        ]
) }}

with

source as (

    select * from {{ source('jaffle_shop', 'jaffle_shop_supplies') }}

),

renamed as (

    select

        ----------  ids
        {{ dbt_utils.generate_surrogate_key(['id', 'sku']) }} as supply_uuid,
        id as supply_id,
        sku as product_id,

        ---------- properties
        name as supply_name,
        (cost / 100.0) as supply_cost,
        perishable as is_perishable_supply

    from source

)

select * from renamed