CREATE EXTERNAL TABLE IF NOT EXISTS step_trainer_landing (
    sensorReadingTime string,
    serialNumber string,
    distanceFromObject int
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://stedi-d609-ne/step_trainer_landing/'
TBLPROPERTIES ('classification'='json');
