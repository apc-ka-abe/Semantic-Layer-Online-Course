
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