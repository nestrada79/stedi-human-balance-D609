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
Filter customer records to include only those who agreed to share their data for research (`shareWithResearchAsOfDate IS NOT NULL`).

**Implementation Highlights:**
- Created in AWS Glue Studio (visual ETL).
- Used a SQL Query transform to filter the dataset.
- Wrote the sanitized output to the Data Catalog table `customer_trusted`.
- IAM Role: `AWSGlueServiceRole`.

**Validation in Athena:**

    SELECT COUNT(*) FROM customer_trusted;

Result returned: **482** rows (correct).

**Artifacts Included:**
- `screenshots/customer_trusted_run.png`
- `screenshots/customer_trusted_ETL.png`
- `screenshots/customer_trusted.png`
- `glue_jobs/customer_trusted.py`

---

### Trusted Zone – ETL Job #2 Complete

### `accelerometer_landing_to_trusted`

**Purpose:**  
Filter accelerometer readings to include only data from customers who consented to share their information for research.

**Implementation Highlights:**
- Created in AWS Glue Studio (visual ETL).
- Two source nodes:
  - `accelerometer_landing`
  - `customer_trusted`
- A SQL Query transform performed the join:

        SELECT myAccel.*
        FROM myAccel
        JOIN myCust
            ON myAccel.user = myCust.email;

- Retained only accelerometer fields in the output.
- Wrote sanitized results to the `accelerometer_trusted` Data Catalog table.
- IAM Role: `AWSGlueServiceRole`.

**Validation in Athena:**

    SELECT COUNT(*) FROM accelerometer_trusted;

Result returned: **40981** rows (correct).

**Artifacts Included:**
- `screenshots/accelerometer_trusted_run.png`
- `screenshots/accelerometer_trusted_ETL.png`
- `screenshots/accelerometer_trusted.png`
- `glue_jobs/accelerometer_landing_to_trusted.py`


### Curated Zone – ETL Job #1 Complete  

### `customer_trusted_to_curated`

This ETL job produces the curated customer dataset. The goal is to ensure that **only customers who shared their data for research AND have accelerometer activity** are retained for downstream machine learning joins.

### **Purpose**
Create the curated customer table (`customer_curated`) by joining:
- `customer_trusted`  
- `accelerometer_trusted`  

Customers are included **only if** their email appears in the accelerometer_trusted dataset.

### **Implementation Details**
- Built using AWS Glue Studio (Visual ETL).
- Data Sources:
  - `customer_trusted` → alias `customer`
  - `accelerometer_trusted` → alias `accel`
- SQL Transform:
  ```sql
  SELECT DISTINCT customer.*
  FROM customer
  JOIN accel
      ON customer.email = accel.user;
  ```
  `DISTINCT` ensures only unique customers are retained (482 expected).

- Target: AWS Glue Data Catalog → table `customer_curated`
- Format: Parquet
- IAM Role: `AWSGlueServiceRole`

### **Validation in Athena**
```
SELECT COUNT(*) FROM customer_curated;
```

**Result: 482 rows** ✔ (matches rubric)

### **Artifacts Included**
- Script: `glue_jobs/customer_trusted_to_curated.py`
- `screenshots/customer_curated.png`
- `screenshots/customer_curated_ETL.png`
- `screenshots/customer_curated_run.png`

## Next Steps

## 6. Trusted Zone – ETL Job #3  
### `step_trainer_landing_to_trusted`

**Purpose**  
Filter Step Trainer IoT data to include only devices belonging to customers who:
- agreed to share their data
- appear in `customer_curated`

**Implementation**  
- Visual ETL in AWS Glue Studio  
- Inputs:
  - `step_trainer_landing` (alias: stepdata)
  - `customer_curated` (alias: cust)
- SQL Transform:
  ```sql
  SELECT stepdata.*
  FROM stepdata
  WHERE stepdata.serialnumber IN (
      SELECT serialnumber
      FROM cust
  );
  ```
- Output target: Glue Catalog table `step_trainer_trusted` (Parquet)

**Validation in Athena**
```sql
SELECT COUNT(*) FROM step_trainer_trusted;
```

**Result:**  
`14460` rows ✔

**Artifacts**  
- Script: `glue_jobs/step_trainer_landing_to_trusted.py`
- `screenshots/step_trainer_landing_to_trusted_ETL.png`
- `screenshots/step_trainer_landing_to_trusted_run.png`
- `screenshots/step_trainer_trusted_query.png`


## 7. Curated Zone – ETL Job #2  
### `machine_learning_curated`

This ETL job creates the final curated dataset used by Data Scientists to train the STEDI step-detection machine learning model. It joins timestamp-aligned accelerometer readings with the corresponding Step Trainer IoT sensor data.

### **Purpose**
Combine:
- `accelerometer_trusted`  
- `step_trainer_trusted`

using matching timestamps to produce a unified, feature-rich dataset for supervised machine learning.

### **Implementation**
- Built using AWS Glue Studio (Visual ETL).
- Input sources:
  - `accelerometer_trusted` (alias: accel)
  - `step_trainer_trusted` (alias: trainer)
- SQL Transform:
  ```sql
  SELECT
      accel.*,
      trainer.distanceFromObject,
      trainer.sensorReadingTime
  FROM accel
  JOIN trainer
      ON accel.timestamp = trainer.sensorReadingTime;
  ```
- Output target:
  - Glue Catalog table: `machine_learning_curated`
  - Format: Parquet

### **Validation in Athena**
Query:
```sql
SELECT COUNT(*) FROM machine_learning_curated;
```

**Result: 43,681 rows** ✔ (matches rubric)

### **Artifacts**
- Script: `glue_jobs/machine_learning_curated.py`
- `screenshots/machine_learning_curated_ETL.png`
- `screenshots/machine_learning_curated_run.png`
- `screenshots/machine_learning_curated_query.png`

## Notes
Work is performed in the Udacity-provided AWS account.  
All ETL jobs will use the `AWSGlueServiceRole` IAM role.  
Data Catalog tables are pre-created in Athena to ensure stable Glue behavior.
