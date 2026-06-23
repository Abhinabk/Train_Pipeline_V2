with final as (
    select
        train_key,
        class,
        passenger_type,
        booking_type,
        fare_rs,
    from {{ ref('int_fare_details') }}
)

select * from final