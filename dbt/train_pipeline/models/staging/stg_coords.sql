--a better way would have veen to make all stations coordonates fileand upoload to seed once
with stg_coords as(
    select * from read_parquet('s3://train-pipeline-v2/reference/matched_coords/2026-06-07/matched_coords.parquet')
),
station_state as (
select 
    "Station Code" as station_code,
    "Station Name" as station_name
    from{{ ref('station_state_seed') }}
),


final as (
    select 
        current_timestamp as timestamp,
        s.station_code::varchar as station_code,
        s.station_name::varchar as station_name,
        c.longitude::DOUBLE as longitude,
        c.latitude::DOUBLE as latitude
    from stg_coords c 
    join  
    station_state s 
    on s.station_code = c.station_code  
)
select * from final