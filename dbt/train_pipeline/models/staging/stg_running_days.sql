with stg_running_days as (
    select *
    from read_parquet('s3://train-pipeline-v2/silver/all_running_days/*/*.parquet')
),
final as (
    select
        current_timestamp as timestamp,
        train_no::varchar as train_no,
        "days"
    from 
        stg_running_days
)
select * from final