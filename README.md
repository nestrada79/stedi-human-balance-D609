# stedi-human-balance-D609

Repo for the code/data for the Udacity project required for WGU D609
Natasha Estrada

STEDI Human Balance Analytics – Data Lakehouse Project



This repository contains my implementation of the STEDI Human Balance Analytics project using AWS Glue, AWS S3, Athena, and PySpark.

The goal of the project is to build a data lakehouse architecture that processes sensor and customer data and prepares curated datasets for downstream machine learning.



✅ Project Status (Current Progress)

1\. Repository Setup



Created a dedicated repository for the STEDI project.



Added initial folder structure:



glue\_jobs/

landing\_zone/

screenshots/





Added a .gitignore appropriate for Python + Jupyter + VS Code.



2\. AWS S3 Landing Zone Created



Created bucket:



s3://stedi-d609-ne





with the required landing folders:



customer\_landing/

accelerometer\_landing/

step\_trainer\_landing/





Uploaded the original JSON datasets from Udacity to each folder.



3\. Landing Zone Tables Created in Athena



Using AWS Athena + Glue Data Catalog, manually created three external tables:



customer\_landing



accelerometer\_landing



step\_trainer\_landing



Each table was created using SQL DDL to correctly map schema and S3 locations.



Landing row counts validated successfully:



Table	Expected	Actual

customer\_landing	956	956

accelerometer\_landing	81273	81273

step\_trainer\_landing	28680	28680



Screenshots stored in screenshots/.



4\. Trusted Zone: Job #1 Complete



Created and successfully ran the first Glue ETL job:



customer\_landing\_to\_trusted



Purpose:



Filter customer\_landing records to include only those who agreed to share data for research (shareWithResearchAsOfDate IS NOT NULL).



Output written to the pre-created Glue Data Catalog table: customer\_trusted.



The Glue job:



Is built using Glue Studio (visual ETL).



Uses a SQL Query transform for filtering.



Uses the AWSGlueServiceRole IAM role.



Result validation in Athena:

SELECT COUNT(\*) FROM customer\_trusted;





Count returned: 482 (correct)



Screenshots + job script saved in:



screenshots/customer\_trusted.png

glue\_jobs/customer\_landing\_to\_trusted.py



📁 Current Repository Structure

/

├── glue\_jobs/

│   └── customer\_landing\_to\_trusted.py

│

├── screenshots/

│   ├── customer\_landing.png

│   ├── accelerometer\_landing.png

│   ├── step\_trainer\_landing.png

│   ├── customer\_trusted.png

│   ├── customer\_landing\_to\_trusted\_run.png

│   └── customer\_landing\_to\_trusted\_diagram.png

│

├── README.md

└── .gitignore



🔜 Next Steps



These are the upcoming ETL tasks:



Job #2: accelerometer\_landing\_to\_trusted



Join accelerometer\_landing with customer\_trusted



Create accelerometer\_trusted



Job #3: step\_trainer\_landing\_to\_trusted



Filter step trainer data using customer\_curated



Job #4: customer\_trusted\_to\_curated



Identify customers who have accelerometer data



Job #5: machine\_learning\_curated



Join step trainer + accelerometer data into final training dataset



Everything will be added to GitHub as the project progresses.

