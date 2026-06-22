with train_route as (
    select
    t.train_key,
    r.route_order,
    r.station_code
from {{ ref('stg_route_order') }} r
join {{ ref('dim_trains') }} t
on r.train_no = t.train_no
),
final as (
    select 
        t.train_key,
        t.route_order,
        s.station_key 
    from train_route t
    join {{ ref('dim_stations') }} s 
    on t.station_code = s.station_code
)
select * from final 

