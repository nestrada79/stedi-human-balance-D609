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

# Script generated for node customer_trusted
customer_trusted_node1764295067939 = glueContext.create_dynamic_frame.from_catalog(database="default", table_name="customer_trusted", transformation_ctx="customer_trusted_node1764295067939")

# Script generated for node accelerometer_trusted
accelerometer_trusted_node1764295073145 = glueContext.create_dynamic_frame.from_catalog(database="default", table_name="accelerometer_trusted", transformation_ctx="accelerometer_trusted_node1764295073145")

# Script generated for node SQL Query
SqlQuery1891 = '''
SELECT DISTINCT customer.*
FROM customer
JOIN accel
    ON customer.email = accel.user;
'''
SQLQuery_node1764296339417 = sparkSqlQuery(glueContext, query = SqlQuery1891, mapping = {"customer":customer_trusted_node1764295067939, "accel":accelerometer_trusted_node1764295073145}, transformation_ctx = "SQLQuery_node1764296339417")

# Script generated for node customer_curated
customer_curated_node1764296556764 = glueContext.write_dynamic_frame.from_catalog(frame=SQLQuery_node1764296339417, database="default", table_name="customer_curated", additional_options={"enableUpdateCatalog": True, "updateBehavior": "LOG"}, transformation_ctx="customer_curated_node1764296556764")

job.commit()