USE powergrid;

-- 3.1 Last 10 records for a sensor
-- SELECT * FROM sensor_data WHERE sid = ... AND day = ... LIMIT 10;

-- 3.2 Total alerts today
SELECT count(*) FROM regional_alerts WHERE region = 'Algiers' AND day = '2024-05-14';

-- 3.3 Average consumption
-- SELECT avg(kw_val) FROM sensor_data WHERE sid = ... AND day = ...;

-- 3.4 Why no ALLOW FILTERING?
-- Filtering across partitions is slow and non-scalable in Cassandra.
