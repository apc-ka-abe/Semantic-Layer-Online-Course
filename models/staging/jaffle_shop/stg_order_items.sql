{{ config(
    post_hook=[
        "OPTIMIZE ka_abe.ka_abe_dbt_silver.stg_orders;"
        ]
) }}

with

source as (

    select * from {{ source('jaffle_shop', 'jaffle_shop_items') }}

),

renamed as (

    select

        ----------  ids
        id as order_item_id,
        order_id,

        ---------- properties
        sku as product_id

    from source

)

select * from renamed