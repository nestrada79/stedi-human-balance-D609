CREATE EXTERNAL TABLE step_trainer_trusted (
    sensorReadingTime bigint,
    serialNumber string,
    distanceFromObject double
)
STORED AS PARQUET
LOCATION 's3://stedi-d609-ne/step_trainer_trusted/';