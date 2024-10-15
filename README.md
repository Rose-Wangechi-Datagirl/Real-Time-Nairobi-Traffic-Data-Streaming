# **Real-Time Nairobi Traffic Data Streaming and Processing using Apache Kafka & Spark**

## **Table of Contents**
1. [Project Overview](#1-project-overview)  
2. [Project Structure](#2-project-structure)  
3. [Technologies Used](#3-technologies-used)  
4. [Architecture Overview](#4-architecture-overview)  
5. [Setup Instructions](#5-setup-instructions)  
6. [How the Kafka Producer Works](#6-how-the-kafka-producer-works)  
7. [How the Spark Consumer Works](#7-how-the-spark-consumer-works)  
8. [Expected Output](#8-expected-output)  
9. [Challenges Faced](#9-challenges-faced)    

---

## **1. Project Overview**
This project showcases **real-time traffic data streaming** by building an end-to-end pipeline using **Apache Kafka** and **Apache Spark**. The traffic data from **Google Maps API** is ingested into Kafka in real time, processed using **Spark Structured Streaming**, and stored in **CSV files** for future analysis.

This project demonstrates the following **core data engineering concepts**:
- **Real-time data ingestion** via Kafka.
- **Stream processing** with Spark.
- **Checkpointing** and data persistence.
- **Containerized environment** setup using Docker.

The result will be a working data pipeline that manages **real-time data flow** and **distributed data processing.**

---

## **2. Project Structure**
```
├─venv
├── docker-compose.yml          # Docker configuration for Kafka, Zookeeper, and Spark
├── scripts/                    
│   ├── kafka_producer.py       # Kafka producer sending traffic data to Kafka topic
│   ├── spark_consumer.py       # Spark consumer reading and processing data from Kafka
├── appends.json
├── checkpoint/                 # Checkpoint directory for stream progress tracking
└── traffic_data/               # Folder to store processed CSV output
```

---
---

## **3. Technologies Used**
- **Apache Kafka**: Distributed streaming platform for real-time messaging.
- **Apache Spark**: Engine for distributed data processing and streaming analytics.
- **Docker**: To containerize and manage Kafka, Zookeeper, and Spark.
- **Python**: For writing Kafka producer and Spark consumer logic.
- **Google Maps API**: Data source for live traffic data.
- **CSV Files**: For storing the processed data.

---

## **4. Architecture Overview**
This pipeline follows the following **flow of data**:  

1. **Kafka Producer**: Fetches live traffic data from Google Maps API and sends it to a **Kafka topic**.  
2. **Kafka Broker**: Manages the incoming messages (traffic data) and acts as the messaging backbone.
3. **Spark Structured Streaming Consumer**: Reads and processes traffic data from Kafka in real time.  
4. **CSV Output Storage**: The processed data is stored as CSV files on the local filesystem.  
5. **Checkpointing**: Spark uses checkpoints to **track stream progress** and ensure fault-tolerance. 

---

## **5. Setup Instructions**

### **Prerequisites**
- Install **Docker** and **Docker Compose**.  
- Install **Python 3.x** 
- Install **kafka-python pyspark requests**

---

## **6. How the Kafka Producer Works**
The **Kafka Producer** script:
1. Connects to **Google Maps API** and fetches live traffic data.
2. Serializes the data to **JSON format**.
3. Sends the data to a Kafka topic called **`traffic_nairobi`**.

## **7. How the Spark Consumer Works**
The **Spark Structured Streaming Consumer**:
1. Subscribes to the **Kafka topic** (`traffic_nairobi`).
2. Processes the traffic data and prints it to the console.
3. Saves the processed data to **CSV files** and uses **checkpoints** for fault tolerance.

## **8. Output**
- Printed Data: The consumer will print the streamed traffic data to the console.
- Saved Data: The processed data is saved to CSV files in the ./traffic_data directory.

---

## **9. Challenges Faced**
- **Docker Port Conflicts**: Resolved by checking existing services running on local ports.
- **Java Configuration Issues**: Ensured `JAVA_HOME` was properly set.
- **Stream Termination Management**: Used `(timeout=30000)` to stop the stream gracefully.
- **Spark Kafka Intergration**: Used the submit packages command 'spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2 kafka_consumer.py' to resolve conflicts
