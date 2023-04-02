WITH cto_week_trips AS (SELECT DATE_PART('week', datetime) AS week, SUM(quantity) trips
                        FROM trips_vw
                        WHERE {bounding_box} @> origin_coord
                        GROUP BY week)
SELECT {bounding_box}, AVG(trips) average_trips
FROM cto_week_trips;