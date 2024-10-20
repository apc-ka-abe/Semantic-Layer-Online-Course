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