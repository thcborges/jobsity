CREATE TABLE IF NOT EXISTS public.trips
(
    region            varchar(135),
    origin_coord      point,
    destination_coord point,
    datetime          timestamp,
    datasource        varchar(135)
);


-- Allow to aggregate using a POINT data type
CREATE OR REPLACE FUNCTION public.hashpoint(point) RETURNS integer
   LANGUAGE sql IMMUTABLE
   AS 'SELECT hashfloat8($1[0]) # hashfloat8($1[1])';

CREATE OPERATOR CLASS public.point_hash_ops DEFAULT FOR TYPE point USING hash AS
   OPERATOR 1 ~=(point,point),
   FUNCTION 1 public.hashpoint(point);

CREATE VIEW public.trips_vw AS
SELECT region, origin_coord, destination_coord, datetime, datasource, COUNT(1) AS quantity
FROM trips
GROUP BY region, origin_coord, destination_coord, datetime, datasource;
