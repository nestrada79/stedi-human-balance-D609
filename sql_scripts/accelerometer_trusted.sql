CREATE EXTERNAL TABLE IF NOT EXISTS accelerometer_trusted (
    timeStamp string,
    user string,
    x double,
    y double,
    z double
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://stedi-d609-ne/accelerometer_trusted/'
TBLPROPERTIES ('classification'='json');
