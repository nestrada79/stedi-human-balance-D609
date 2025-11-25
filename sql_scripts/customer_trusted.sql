CREATE EXTERNAL TABLE IF NOT EXISTS customer_trusted (
    serialNumber string,
    shareWithPublicAsOfDate string,
    birthday string,
    registrationDate string,
    shareWithResearchAsOfDate string,
    customerName string,
    email string,
    lastUpdateDate string,
    phone string,
    shareWithFriendsAsOfDate string
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://stedi-d609-ne/customer_trusted/'
TBLPROPERTIES ('classification'='json');
