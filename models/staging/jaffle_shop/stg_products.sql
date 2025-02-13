{{ config(
    post_hook=[
        "OPTIMIZE ka_abe.ka_abe_dbt_silver.stg_order_items;"
        ]
) }}
with

source as (

    select * from {{ source('jaffle_shop', 'jaffle_shop_products') }}
),

renamed as (

    select

        ----------  ids
        sku as product_id,

        ---------- properties
        name as product_name,
        type as product_type,
        description as product_description,
        (price / 100.0) as product_price,


        ---------- derived
        case
            when type = 'jaffle' then 1
            else 0
        end as is_food_item,

        case
            when type = 'beverage' then 1
            else 0
        end as is_drink_item

    from source

)

select * from renamed