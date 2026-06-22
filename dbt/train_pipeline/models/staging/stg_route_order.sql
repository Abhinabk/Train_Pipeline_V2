with stg_route_order as (
    select * 
    from read_parquet('s3://train-pipeline-v2/silver/route_order/*/*.parquet')
),
final as (
    select
        current_timestamp as timestamp,
        train_no::varchar as train_no,
        station_code::varchar as station_code,
        station_name::varchar as station_name,
        "order"::INTEGER as "order"
    from stg_route_order
)
select * from final