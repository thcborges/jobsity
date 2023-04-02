-- From the two most commonly appearing regions, which is the latest datasource?
WITH cto_common_regions AS (SELECT region, SUM(quantity) total
                            FROM trips_vw
                            GROUP BY region
                            ORDER BY total DESC
                            LIMIT 2),
     cto_ranked_records AS (SELECT t.datasource, RANK() OVER (PARTITION BY t.region ORDER BY datetime DESC) AS rank
                             FROM trips_vw t
                                      JOIN cto_common_regions cr ON t.region = cr.region)
SELECT datasource
FROM cto_ranked_records
WHERE rank = 1;

-- What regions has the "cheap_mobile" datasource appeared in?
SELECT DISTINCT region
FROM trips_vw
WHERE datasource = 'cheap_mobile';