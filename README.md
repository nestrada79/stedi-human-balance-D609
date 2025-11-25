# STEDI Human Balance Analytics – Data Lakehouse Project

This repository contains my implementation of the STEDI Human Balance Analytics project using **AWS Glue**, **AWS S3**, **Athena**, and **PySpark**.  
The objective of the project is to build a data lakehouse architecture that processes sensor, accelerometer, and customer data and prepares curated datasets for machine learning model development.

## Project Status (Current Progress)

### 1. Repository Setup
- New GitHub repository created specifically for the STEDI project.
- Added initial folder structure:
  ```
  glue_jobs/
  landing_zone/
  screenshots/
  ```
- Added `.gitignore` to exclude Python, Jupyter, and VS Code artifacts.

### 2. AWS S3 Landing Zone Created
A new S3 bucket was created:

```
s3://stedi-d609-ne
```

With the required landing folders:

```
customer_landing/
accelerometer_landing/
step_trainer_landing/
```

Uploaded Udacity's JSON datasets into their corresponding folders.

### 3. Landing Zone Tables in Athena/Glue Catalog
Using AWS Athena, three landing tables were created with SQL DDL:

- `customer_landing`
- `accelerometer_landing`
- `step_trainer_landing`

Schemas were defined explicitly to match input JSON data.  
All three tables were validated through row counts:

| Table Name              | Expected Count | Actual Count |
|-------------------------|----------------|--------------|
| customer_landing        | 956            | 956          |
| accelerometer_landing   | 81273          | 81273        |
| step_trainer_landing    | 28680          | 28680        |

Screenshots stored in `screenshots/`.

### 4. Trusted Zone – ETL Job #1 Complete
Created and successfully executed Glue ETL job:

### `customer_landing_to_trusted`

**Purpose:**  
Filter customer records to include only those who agreed to share their data for research  
(`shareWithResearchAsOfDate IS NOT NULL`).

**Implementation Highlights:**
- Created in AWS Glue Studio (visual ETL).
- Used SQL Query transform to filter the dataset.
- Output written to the pre-created Data Catalog table `customer_trusted`.
- IAM Role: `AWSGlueServiceRole`

**Validation in Athena:**

```sql
SELECT COUNT(*) FROM customer_trusted;
```

Result returned: **482** rows (correct)

Artifacts included:
- `screenshots/customer_landing_to_trusted_run.png`
- `screenshots/customer_landing_to_trusted_ETL.png`
- `screenshots/customer_landing_to_trusted_SQL_validation.png` 
- `glue_jobs/customer_landing_to_trusted.py`

### Job #2 – accelerometer_landing_to_trusted

This Glue Studio ETL job filters accelerometer data to include only readings from customers who agreed to share their data for research.

**Process:**
1. Load data from:
   - `accelerometer_landing`
   - `customer_trusted`
2. Perform an inner join on:
```accelerometer_landing.user = customer_trusted.email```
3. Retain only accelerometer fields.
4. Write the sanitized results to the `accelerometer_trusted` table in the Trusted Zone.

**Outputs:**
- Trusted table: `accelerometer_trusted`
- Row count verified in Athena: **40981**
- Script: `glue_jobs/accelerometer_landing_to_trusted.py`
- Screenshot: `screenshots/accelerometer_trusted.png`

## Next Steps

### Job #3 – step_trainer_landing_to_trusted
- Filter step trainer data using customer_curated

### Job #4 – customer_trusted_to_curated
- Include only customers who have accelerometer Trusted Zone data

### Job #5 – machine_learning_curated
- Join accelerometer_trusted + step_trainer_trusted by timestamp
- Produce final curated dataset for ML

All scripts and screenshots will be added as the project progresses.

## Submission Requirements Covered So Far
- Landing zone created in S3  
- Landing tables created in Athena  
- Row counts validated for landing zone  
- Trusted zone Job #1 completed  
- Trusted table `customer_trusted` validated (482 rows)  
- Glue script downloaded and included  

## Notes
Work is performed in the Udacity-provided AWS account.  
All ETL jobs will use the `AWSGlueServiceRole` IAM role.  
Data Catalog tables are pre-created in Athena to ensure stable Glue behavior.
