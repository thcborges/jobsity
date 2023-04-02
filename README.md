# Jobsity Challenge

This challenge will evaluate your proficiency in Data Engineering, and your knowledge in
Software development as well.


## Assignment

Your task is to build an automatic process to ingest data on an on-demand basis. The data
represents trips taken by different vehicles, and include a city, a point of origin and a destination.
[This CSV](https://drive.google.com/file/d/14JcOSJAWqKOUNyadVZDPm7FplA7XYhrU/view) file gives you a small sample of the data your solution will have to handle. We would
like to have some visual reports of this data, but in order to do that, we need the following
features.
We do not need a graphical interface. Your application should preferably be a REST API, or a
console application.


## Mandatory Features

- There must be an automated process to ingest and store the data.
- Trips with similar origin, destination, and time of day should be grouped together.
- Develop a way to obtain the weekly average number of trips for an area, defined by a bounding box (given by coordinates) or by a region.
- Develop a way to inform the user about the status of the data ingestion without using a polling solution.
- The solution should be scalable to 100 million entries. It is encouraged to simplify the data by a data model. Please add proof that the solution is scalable.
● Use a SQL database.


## Bonus features

- Containerize your solution.
- Sketch up how you would set up the application using any cloud provider (AWS, Google Cloud, etc).
- Include a .sql file with queries to answer these questions:
  -  From the two most commonly appearing regions, which is the latest datasource?
  -  What regions has the "cheap_mobile" datasource appeared in?


## The developed application

To ingest a 100 million entries data, I developed a Kafka based application. 
There is one job to read the data (`read-trips`) and there is another one to load the data in a PostgreSQL database.(`load-trips`).
And there is one job to create replicated entries from the [CSV file](https://drive.google.com/file/d/14JcOSJAWqKOUNyadVZDPm7FplA7XYhrU/view) (`fake-trips`).

The `load-data` job is slower then the `read-trips` or `fake-trips` jobs and 
I couldn't find a method to watch track how is queue of the kafka topic. 
In a production environment would be recommended to install the application in a cluster
replicating the `load_trips` and `kafka` docker services to use more partitions 
what will make the database ingestion faster. 
However the Kafka solution allow to query the data even it is not entirely loaded. 
Using Kafka inside the company systems also allows to have
real time or near real time data in the database.

## Configuring the application

### .env file

- **LOG_LEVEL**: log level to be displayed. Other levels will be displayed inside `./jobsity/log` folder separating it by date and rotating the log automatically.
- **TRIPS_TOTAL**: How much fake trips you want to generate.
- **POSTGRES_XXXX**: Postgres configuration
- **DATA_PATH**: The path to the data storage. <mark>The CSV File must be stored inside this a folder called `input` in this path. For example `DATA_ROOT/input/trips.csv`</mark>
- **BOOTSTRAP_SERVERS**: The address to kafka container. Just replicate as it is in `.env.example`

## Creating and starting the application

Just need to execute the bellow command.

```bash
docker-compose up -d --scale load_trips=4
```

This will create and start the application containers.

- *Zookeper*
- *Kafka*
- *db* 
- *load_trips_1*
- *load_trips_2*
- *load_trips_3*
- *load_trips_4*
- *app*

The `load_trips` containers are a loop process to ingest the data
in the database.

It is possible to execute any other job using the app container.

## Reading and loading data

To read the data from the CSV file stored in <mark>`DATA_ROOT/input`</mark> you can execute the bellow command:

```bash
docker-compose exec app jobsity read-trips
```

Then the process will the `trip.csv` file and send it to 'trips' Kafka topic. The `load_trips` job will receive the data and store it in the database.

You can also generate replicated data from `trips.csv` setting the **TRIPS_TOTAL** environment variable and file using the bellow command.

```bash
docker-compose exec app jobsity fake-trips
```

## Loaded data

The data will be loaded in `trips` table but, the queries execute over the `trips_vw` view that aggregate the data contained int `trips` table.

## Retrieving information

It is not necessary to wait until the `load_trips` jobs ends the Kafka topic queue
to retrieve information from the database. 
You can query the average weekly number of trips using the bellow commands:

### By region

```
docker-compose exec app jobsity trips-by-region <REGION>
```

Where `<REGION>` needs to be replaced by the required region.

### By bounding box

```
docker-compose exec app jobsity trips-by-region <GEOMETRY>
```

Where `<GEOMETRY>` is restricted to the [PostgreSQL GEOMETRY functions](https://www.postgresql.org/docs/current/functions-geometry.html#FUNCTIONS-GEOMETRY-CONV-TABLE). 
It is necessary to implement a validator to the input data.

Examples:

```
docker-compose exec app jobsity trips-by-region "polygon('(7.557332202515,45.043466919307), (7.557332202516,45.043466919308), (8, 40)')"

docker-compose exec app jobsity trips-by-region "box('(7.557332202515,45.043466919307), (7.557332202516,45.043466919308)')"
```

## Bonus questions:

[answers.sql](jobsity/core/sql/answers.sql)

- From the two most commonly appearing regions, which is the latest datasource?
  ```sql
    WITH cto_common_regions AS (SELECT region, SUM(quantity) total
                                FROM trips_vw
                                GROUP BY region
                                ORDER BY total DESC
                                LIMIT 2),
        cto_ranked_records AS (SELECT t.datasource, 
                                      RANK() OVER (
                                            PARTITION BY t.region 
                                            ORDER BY datetime DESC
                                      ) AS rank
                                FROM trips_vw t
                                        JOIN cto_common_regions cr
                                          ON t.region = cr.region)
    SELECT datasource
    FROM cto_ranked_records
    WHERE rank = 1;
  ```
- What regions has the "cheap_mobile" datasource appeared in?
  ```sql
    SELECT DISTINCT region
    FROM trips_vw
    WHERE datasource = 'cheap_mobile';
  ```
