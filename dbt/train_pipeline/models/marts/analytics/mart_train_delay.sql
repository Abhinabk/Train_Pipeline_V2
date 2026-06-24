with delay as (
    select
        station_key,
        train_key,
        delay
    from {{ ref('fact_delay') }}
),
train_delay as (
    select 
        t.train_no,
        Round(avg(d.delay),2) as avg_delay 
    from delay d 
    join {{ ref('dim_trains') }} t
    on d.train_key = t.train_key
    group by t.train_no
)
select * from train_delay

