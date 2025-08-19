--- Tells dbt to create a physical table in your data warehouse when this model is run.
{{config(
    materialized= 'table', 
    unique_key= 'id'
)}}

with source as(
    -- This macro pulls data from a declared source in sources.yml.
    -- dev: The source name (your logical grouping).
    --  raw_weather_data: The actual table name in the database.
    select * from {{ source ('dev', 'raw_weather_data')}}
),
de_dup as (
    select *,
    row_number() over(partition by time order by inserted_at) as rn
    from source
)


select  
    id,
    city,
    temperature,
    weather_descriptions,
    wind_speed,
    time as weather_time_local,
    -- ufc_offset || 'hours': Concatenates the number with the string 'hours', producing something like '9hours'.
    --  ::interval: Casts that string into a PostgreSQL interval, e.g., interval '9 hours'.
    -- inserted_at + interval: Adds the interval to the timestamp, giving you the local time.
    (inserted_at + (ufc_offset || 'hours')::interval) as inserted_at_local
from de_dup
where rn = 1