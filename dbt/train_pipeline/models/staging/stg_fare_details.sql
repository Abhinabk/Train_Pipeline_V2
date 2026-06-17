with stg_fare_details as (

    select * 
    from read_parquet('s3://train-pipeline-v2/silver/fare_details/*/*.parquet')
),

final as (
    select 
        current_timestamp as timestamp,
        train_no,
        "class",
        "Adult (Normal)",
        "Adult (Tatkal)",
        "Child (Normal)",
        "Child (Tatkal)",
        "Senior Female (Normal)",
        "Senior Female (Tatkal)",
        "Senior Male (Normal)",
        "Senior Male (Tatkal)"
    from stg_fare_details
    )
select * from final