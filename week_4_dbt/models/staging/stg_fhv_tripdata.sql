{{
    config(materialized='view')
}}

select
    cast(pickup_datetime as timestamp) as pickup_datetime,
    cast(dropOff_datetime as timestamp) as dropoff_datetime,
    cast(PUlocationID as integer) as pickup_locationid,
    cast(DOlocationID as integer) as dropoff_locationid,
    cast(SR_Flag as integer) as sr_flag, 
    dispatching_base_num,			
    Affiliated_base_number as affiliated_base_num

from {{ source('staging', 'fhv_trips_clustered') }}

-- dbt build --m <model.sql> --var 'is_test_run: false'
{% if var('is_test_run', default=true) %}

  limit 100

{% endif %}
