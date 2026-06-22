with stg_route_order as (
    select * 
    from read_parquet('s3://train-pipeline-v2/silver/route_order/*/*.parquet')
),
station_state as (
select 
    "Station Code" as station_code,
    "Station Name" as station_name
    from{{ ref('station_state_seed') }}
),

final as (
    select
        DISTINCT
            r.train_no::varchar as train_no,
            s.station_code::varchar as station_code,
            s.station_name::varchar as station_name,
            r.order::INTEGER as route_order
    from stg_route_order r
    join  
    station_state s 
    on s.station_code = r.station_code
)
select * from final