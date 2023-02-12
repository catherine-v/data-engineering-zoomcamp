create or replace external table `smiling-breaker-376117.trips_data_all.fhv_trips_external`
options (
  format='csv',
  uris=['gs://dtc_data_lake_smiling-breaker-376117/data/fhv/*']
);

create or replace table `smiling-breaker-376117.trips_data_all.fhv_trips`
as select * from `smiling-breaker-376117.trips_data_all.fhv_trips_external`;

-- Q1
select count(*) from `smiling-breaker-376117.trips_data_all.fhv_trips_external`;

-- Q2
select count(distinct affiliated_base_number) from `smiling-breaker-376117.trips_data_all.fhv_trips_external`;
select count(distinct affiliated_base_number) from `smiling-breaker-376117.trips_data_all.fhv_trips`;

-- Q3
select count(*)
from `smiling-breaker-376117.trips_data_all.fhv_trips`
where PUlocationID is null and DOlocationID is null;

-- Q5
create or replace table `smiling-breaker-376117.trips_data_all.fhv_trips_clustered`
partition by date(pickup_datetime) 
cluster by affiliated_base_number
as select * from `smiling-breaker-376117.trips_data_all.fhv_trips`;

select count(distinct affiliated_base_number)
from `smiling-breaker-376117.trips_data_all.fhv_trips`
where date(pickup_datetime) between '2019-03-01' and '2019-03-31';

select count(distinct affiliated_base_number)
from `smiling-breaker-376117.trips_data_all.fhv_trips_clustered`
where date(pickup_datetime) between '2019-03-01' and '2019-03-31';
