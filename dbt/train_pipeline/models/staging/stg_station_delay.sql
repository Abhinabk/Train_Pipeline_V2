with stg_station_delay as (
    select *
    from read_parquet('s3://train-pipeline-v2/silver/station_delay/*/*.parquet')
),

station_state as (
select 
    "Station Code" as station_code
    from{{ ref('station_state_seed') }}
),

final as (
    select
        distinct
        train_no::varchar as train_no,
        date::DATE as "date",
        s.station_code::VARCHAR as station_code,
        delay::DOUBLE as delay
    from stg_station_delay d
    join station_state s
    on d.station_code = s.station_code
)

select * from final 


select
    min(date),
    max(date),
    count(*)
from read_parquet(
's3://train-pipeline-v2/silver/station_delay/2026-06-21/*.parquet'
);