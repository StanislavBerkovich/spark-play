from pyspark.sql import SparkSession
from pyspark.sql.types import  StructType, StructField, StringType, IntegerType
from pyspark.sql.functions import expr, from_json, col, concat


# Create a SparkSession
spark = SparkSession.builder \
    .appName("SparkApplication") \
    .getOrCreate()

schema = StructType([
    StructField("user_id", IntegerType()),
    StructField("name", StringType()),
    StructField("email", StringType()),
])


# Read from Kafka topic with the specified schema
kafka_df = spark \
    .read \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "user_registration") \
    .load() 

parsed_df = kafka_df \
    .selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select(col("data.user_id").alias("id"), "data.name", "data.email")


# Write the transformed data to PostgreSQL
parsed_df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://postgres:5432/sparkdb") \
    .option("dbtable", "user_data") \
    .option("user", "sparkuser") \
    .option("driver", "org.postgresql.Driver")\
    .option("password", "sparkpass") \
    .mode("append") \
    .save()

# Stop the SparkSession
spark.stop()
