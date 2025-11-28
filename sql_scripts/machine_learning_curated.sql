CREATE EXTERNAL TABLE machine_learning_curated (
    timestamp bigint,
    user string,
    x double,
    y double,
    z double,
    distanceFromObject double,
    sensorReadingTime bigint
)
STORED AS PARQUET
LOCATION 's3://stedi-d609-ne/machine_learning_curated/';
