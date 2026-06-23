with fare_details as (
    select
        train_no,
        class,
        replace("Adult (Normal)", 'Rs ', '')::integer as adult_normal,
        replace("Adult (Tatkal)", 'Rs ', '')::integer as adult_tatkal,
        replace("Child (Normal)", 'Rs ', '')::integer as child_normal,
        replace("Child (Tatkal)", 'Rs ', '')::integer as child_tatkal,
        replace("Senior Female (Normal)", 'Rs ', '')::integer as senior_female_normal,
        replace("Senior Female (Tatkal)", 'Rs ', '')::integer as senior_female_tatkal,
        replace("Senior Male (Normal)", 'Rs ', '')::integer as senior_male_normal,
        replace("Senior Male (Tatkal)", 'Rs ', '')::integer as senior_male_tatkal
    from {{ ref('stg_fare_details') }}
),
fare_long as (
    UNPIVOT fare_details
    on 
        COLUMNS(* EXCLUDE(train_no,class))
    into
        name passenger
        value fare_rs
),
booking as (
    select
        train_no,
        class,
        regexp_extract(passenger,'^(.*)_(normal|tatkal)$',1) as passenger_type,
        regexp_extract(passenger,'_(normal|tatkal)$',1) as booking_type,
        fare_rs  
    from fare_long
),
final as (
    select
        b.* exclude(train_no),
        t.train_key 
    from booking b 
    join {{ref("dim_trains")}} t
    on b.train_no = t.train_no
)
select * from final