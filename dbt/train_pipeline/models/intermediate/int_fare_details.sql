{# with fare_details as (
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
with fare_long as (
    UNPIVOT fare_details
    on 
        * except(train_no,class)
    into
        name passenger

) #}