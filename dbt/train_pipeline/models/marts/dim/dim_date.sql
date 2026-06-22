{#  generates a range of date from 2025 to 2030 used to determine weekends weekdays
    can be futher augmented with hodidays just by adding a is_holidy column and a 
    railway holiday seed file or amke another dim_holidy tabke with date_key as fk
 #}
with dates as (
    select
        full_date::date as full_date
    from generate_series(date '2025-01-01',date '2028-12-31', interval '1 day') as t(full_date)
),

final as (
    select
        strftime(full_date,'%Y%m%d')::INT as date_key,
        full_date,
        year(full_date) as year,
        month(full_date) as month,
        monthname(full_date) as month_name,
        day(full_date) as day_of_month,
        dayname(full_date) as day_of_week_name,
        isodow (full_date) as day_of_week_num,
        isodow (full_date) in (6,7) as is_weekend --7=sun 6= sat
    from dates
)
select * from final 