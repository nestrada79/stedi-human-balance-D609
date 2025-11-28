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
customer_trusted_node1764040028132 = glueContext.create_dynamic_frame.from_catalog(database="default", table_name="customer_trusted", transformation_ctx="customer_trusted_node1764040028132")

# Script generated for node accelerometer_landing
accelerometer_landing_node1764039994716 = glueContext.create_dynamic_frame.from_catalog(database="default", table_name="accelerometer_landing", transformation_ctx="accelerometer_landing_node1764039994716")

# Script generated for node join_accel_customer
SqlQuery1240 = '''
SELECT myAccel.*
FROM myAccel
JOIN myCust
    ON myAccel.user = myCust.email

'''
join_accel_customer_node1764040117727 = sparkSqlQuery(glueContext, query = SqlQuery1240, mapping = {"myCust":customer_trusted_node1764040028132, "myAccel":accelerometer_landing_node1764039994716}, transformation_ctx = "join_accel_customer_node1764040117727")

# Script generated for node accelerometer_trusted
accelerometer_trusted_node1764040640480 = glueContext.write_dynamic_frame.from_catalog(frame=join_accel_customer_node1764040117727, database="default", table_name="accelerometer_trusted", transformation_ctx="accelerometer_trusted_node1764040640480")

job.commit()