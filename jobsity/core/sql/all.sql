create table public.trips
(
    region            varchar(135),
    origin_coord      point,
    destination_coord point,
    datetime          timestamp,
    datasource        varchar(135)
);

CREATE OR REPLACE FUNCTION public.hashpoint(point) RETURNS integer
    LANGUAGE sql
    IMMUTABLE
AS
'SELECT hashfloat8($1[0]) # hashfloat8($1[1])';

DROP OPERATOR CLASS IF EXISTS public.point_hash_ops USING hash;
CREATE OPERATOR CLASS public.point_hash_ops DEFAULT FOR TYPE point USING hash AS
    OPERATOR 1 ~=(point,point),
    FUNCTION 1 public.hashpoint(point);


CREATE OR REPLACE VIEW public.trips_vw AS
SELECT region, origin_coord, destination_coord, datetime, datasource, COUNT(1) AS quantity
FROM trips
GROUP BY region, origin_coord, destination_coord, datetime, datasource;

SELECT *
FROM teste
ORDER BY region, origin_coord[0];

SELECT COUNT(1)
FROM teste;

SELECT COUNT(1)
FROM trips;

WITH cto_week_trips AS (
    SELECT region, DATE_PART('week', datetime) AS week, SUM(quantity) trips
    FROM trips_vw
    GROUP BY region
)
SELECT region, AVG(trips) average_trips
FROM cto_week_trips
GROUP BY region
ORDER BY average_trips DESC;

SELECT region, datetime, DATE_PART('week', datetime) AS week, SUM(quantity)
FROM teste
WHERE polygon('(7.557332202515,45.043466919307), (7.557332202516,45.043466919308), (8, 40)') @> origin_coord
GROUP BY region, datetime;


-- From the two most commonly appearing regions, which is the latest datasource?
WITH cto_common_regions AS (SELECT region, SUM(quantity) total
                            FROM trips_vw
                            GROUP BY region
                            ORDER BY total DESC
                            LIMIT 2),
     cto_ranked_records AS (SELECT t.datasource, RANK() OVER (PARTITION BY t.region ORDER BY datetime DESC) AS rank
                             FROM trips_vw t
                                      JOIN cto_common_regions cr ON t.region = cr.region
                             ORDER BY t.region, t.datetime DESC)
SELECT datasource
FROM cto_ranked_records
WHERE rank = 1;

-- What regions has the "cheap_mobile" datasource appeared in?
SELECT DISTINCT region
FROM trips_vw
WHERE datasource = 'cheap_mobile';