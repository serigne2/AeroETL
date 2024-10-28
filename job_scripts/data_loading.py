import boto3
import json
import os
import psycopg2
from datetime import datetime

def load_data_to_s3(data, city):
    s3 = boto3.client('s3')
    bucket_name = os.getenv("S3_BUCKET_NAME")
    file_name = f"{city}_weather_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=json.dumps(data)
    )
    print(f"Data for {city} loaded to S3 bucket {bucket_name} as {file_name}")

def load_data_to_rds(data):
    conn = psycopg2.connect(
        dbname=os.getenv("RDS_DB_NAME"),
        user=os.getenv("RDS_USER"),
        password=os.getenv("RDS_PASSWORD"),
        host=os.getenv("RDS_HOST"),
        port=os.getenv("RDS_PORT")
    )
    cursor = conn.cursor()
    
    for entry in data:
        cursor.execute("""
            INSERT INTO weather_data (city, temperature, humidity, pressure, weather_description, classification, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, to_timestamp(%s))
        """, (
            entry["city"],
            entry["temperature_celsius"],
            entry["humidity"],
            entry["pressure"],
            entry["weather_description"],
            entry["weather_classification"],
            entry["timestamp"]
        ))
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Data loaded to RDS successfully")
