WITH cto_week_trips AS (SELECT region, DATE_PART('week', datetime) AS week, SUM(quantity) trips
                        FROM trips_vw
                        WHERE region = %s
                        GROUP BY region, week)
SELECT region, AVG(trips) average_trips
FROM cto_week_trips
GROUP BY region
ORDER BY average_trips DESC;