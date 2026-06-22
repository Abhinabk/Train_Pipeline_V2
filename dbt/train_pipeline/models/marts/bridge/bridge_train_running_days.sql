select 
    d.train_key,
    i.days as running_days
from {{ ref('int_running_days') }} i
join {{ ref('dim_trains') }} d
on i.train_no = d.train_no