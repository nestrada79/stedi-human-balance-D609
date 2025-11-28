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

# Script generated for node Amazon S3 customer_landing
AmazonS3customer_landing_node1764348796021 = glueContext.create_dynamic_frame.from_options(format_options={"multiLine": "false"}, connection_type="s3", format="json", connection_options={"paths": ["s3://stedi-d609-ne/customer_landing/"], "recurse": True}, transformation_ctx="AmazonS3customer_landing_node1764348796021")

# Script generated for node SQL Query
SqlQuery2179 = '''
SELECT *
FROM myDataSource
WHERE shareWithResearchAsOfDate IS NOT NULL;

'''
SQLQuery_node1764023756368 = sparkSqlQuery(glueContext, query = SqlQuery2179, mapping = {"myDataSource":AmazonS3customer_landing_node1764348796021}, transformation_ctx = "SQLQuery_node1764023756368")

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1764023999729 = glueContext.write_dynamic_frame.from_catalog(frame=SQLQuery_node1764023756368, database="default", table_name="customer_trusted", additional_options={"enableUpdateCatalog": True, "updateBehavior": "LOG"}, transformation_ctx="AWSGlueDataCatalog_node1764023999729")

job.commit()