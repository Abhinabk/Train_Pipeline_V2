select 
    train_no,
    UNNEST(days) as days 
    
from {{ref('stg_running_days')}}