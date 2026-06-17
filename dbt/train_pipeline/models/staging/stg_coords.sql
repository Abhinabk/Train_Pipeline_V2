--a better way would have veen to make all stations coordonates fileand upoload to seed once
with stg_coords as(
    select * from read_parquet('s3://train-pipeline-v2/reference/matched_coords/2026-06-07/matched_coords.parquet')
),
final as (
    select 
        current_timestamp as timestamp,
        station_code,
        station_name,
        longitude,
        latitude
    from stg_coords
)
select * from final