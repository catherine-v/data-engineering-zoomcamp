-- Question 3
select
    count(2)
from 
	green_tripdata_trip
where 1=1
	and lpep_pickup_datetime::date = '2019-01-15'
	and lpep_dropoff_datetime::date = '2019-01-15'
;

-- Question 4
select
	lpep_pickup_datetime::date,
	max(trip_distance) as max_distance
from 
	green_tripdata_trip
group by 1
order by max_distance desc
;

-- Question 5
select
	passenger_count, 
	count(1) as cnt
from
	green_tripdata_trip
where 1=1
	and lpep_pickup_datetime::date = '2019-01-01'
	and passenger_count in (2, 3)
group by 1
;

-- Question 6
select
	t.tip_amount,
	dz."LocationID",
	dz."Borough",
	dz."Zone"
from
	green_tripdata_trip t
join
	zone_lookup pz 
		on t."PULocationID" = pz."LocationID"
join
	zone_lookup dz 
		on t."DOLocationID" = dz."LocationID"
where 1=1
	and pz."Zone" = 'Astoria'
order by 
	tip_amount desc
;
