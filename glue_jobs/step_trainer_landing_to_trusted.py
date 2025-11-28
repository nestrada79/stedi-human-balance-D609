import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node step_trainer_landing
step_trainer_landing_node1764300689973 = glueContext.create_dynamic_frame.from_catalog(database="default", table_name="step_trainer_landing", transformation_ctx="step_trainer_landing_node1764300689973")

# Script generated for node customer_curated
customer_curated_node1764300771856 = glueContext.create_dynamic_frame.from_catalog(database="default", table_name="customer_curated", transformation_ctx="customer_curated_node1764300771856")

# Script generated for node SQL Query
SqlQuery1794 = '''
SELECT stepdata.*
FROM stepdata
WHERE stepdata.serialnumber IN (
    SELECT serialnumber
    FROM cust
);

'''
SQLQuery_node1764300791119 = sparkSqlQuery(glueContext, query = SqlQuery1794, mapping = {"cust":customer_curated_node1764300771856, "stepdata":step_trainer_landing_node1764300689973}, transformation_ctx = "SQLQuery_node1764300791119")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1764300865942 = glueContext.write_dynamic_frame.from_catalog(frame=SQLQuery_node1764300791119, database="default", table_name="step_trainer_trusted", additional_options={"enableUpdateCatalog": True, "updateBehavior": "UPDATE_IN_DATABASE"}, transformation_ctx="AWSGlueDataCatalog_node1764300865942")

job.commit()