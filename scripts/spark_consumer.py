from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json,col
from pyspark.sql.types import LongType, StringType, StructType, DoubleType

#initialise spark session
spark= SparkSession.builder \
    .appName("KafkaSparkTrafficConsumer") \
    .getOrCreate()

#define schema for the traffic data
traffic_schema= StructType() \
        .add("origin", StringType()) \
        .add("destination", StringType()) \
        .add("distance_text", StringType()) \
        .add("distance_value", LongType()) \
        .add("duration_text", StringType()) \
        .add("duration_value", LongType()) \
        .add("duration_in_traffic_text", StringType()) \
        .add("duration_in_traffic_value", LongType()) \
        .add("congestion_level", DoubleType()) \
        .add("timestamp", StringType())  # ISO format timestamp as a string

# read from Kafka topic traffic_nairobi
df= spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "traffic_nairobi") \
    .load()

#decode message and convert to JSON
traffic_df= df.selectExpr("CAST(value as STRING)") \
        .select(from_json(col("value"), traffic_schema).alias("data")) \
        .select("data.*")


#process the data and print it out in the console 
console_query= traffic_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

#save the streamed data into a csv
csv_query = traffic_df \
    .writeStream \
    .outputMode("append") \
    .format("csv") \
    .option("checkpointLocation", "./checkpoint") \
    .option("path", "./traffic_data") \
    .start()


try:
    console_query.awaitTermination(timeout=30000)  # Console streaming to stop after 30 seconds if no new data 
    csv_query.awaitTermination(timeout=30000)      # CSV timeout
except Exception as e:
    print(f"Streaming stopped with error: {e}")