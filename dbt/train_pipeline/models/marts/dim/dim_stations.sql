with stations as (
    select 
        "station code" as station_code,
        "station name" as station_name,
        "Longitude" as longitude,
        "Latitude" as latitude,
        "State" as state,
        "District" as district 
    from {{ ref('station_state_seed') }}
),

final as (
    select
        {{dbt_utils.generate_surrogate_key(['station_code'])}} as station_key,
        *
    from stations
)

select * from final