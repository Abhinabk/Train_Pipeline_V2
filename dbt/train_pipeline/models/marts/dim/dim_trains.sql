with trains as (
    select
        number::varchar as train_no,
        name::varchar as train_name
    from {{ ref('trains_seed') }}
),
final as (
    select 
        {{dbt_utils.generate_surrogate_key(['train_no'])}} as train_key,
        *
    from trains
)
select * from final