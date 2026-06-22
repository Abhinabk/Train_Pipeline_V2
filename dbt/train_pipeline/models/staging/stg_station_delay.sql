with stg_station_dealy as (
    select *
    from read_parquet('s3://train-pipeline-v2/silver/station_delay/*/*.parquet')
),
final as (
    select
        current_timestamp as timestamp,
        train_no::varchar as train_no,
        date::DATE as "date",
        station_code::VARCHAR as station_code,
        delay::DOUBLE as delay
    from stg_station_dealy
)
select * from final