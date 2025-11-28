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

# Script generated for node step_trainer_trusted
step_trainer_trusted_node1764302620208 = glueContext.create_dynamic_frame.from_catalog(database="default", table_name="step_trainer_trusted", transformation_ctx="step_trainer_trusted_node1764302620208")

# Script generated for node accelerometer_trusted
accelerometer_trusted_node1764302666901 = glueContext.create_dynamic_frame.from_catalog(database="default", table_name="accelerometer_trusted", transformation_ctx="accelerometer_trusted_node1764302666901")

# Script generated for node SQL Query
SqlQuery2048 = '''
SELECT
    accel.*,
    trainer.distanceFromObject,
    trainer.sensorReadingTime
FROM accel
JOIN trainer
    ON accel.timestamp = trainer.sensorReadingTime;
'''
SQLQuery_node1764302695434 = sparkSqlQuery(glueContext, query = SqlQuery2048, mapping = {"accel":accelerometer_trusted_node1764302666901, "trainer":step_trainer_trusted_node1764302620208}, transformation_ctx = "SQLQuery_node1764302695434")

# Script generated for node machine_learning_curated
machine_learning_curated_node1764302725734 = glueContext.write_dynamic_frame.from_catalog(frame=SQLQuery_node1764302695434, database="default", table_name="machine_learning_curated", additional_options={"enableUpdateCatalog": True, "updateBehavior": "UPDATE_IN_DATABASE"}, transformation_ctx="machine_learning_curated_node1764302725734")

job.commit()