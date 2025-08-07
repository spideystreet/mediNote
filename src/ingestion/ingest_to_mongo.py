import json
from pymongo import MongoClient
import os

def ingest_to_mongodb():
    mongo_host = "localhost"
    mongo_port = os.getenv("MONGO_PORT", "27017")
    mongo_uri = f"mongodb://{mongo_host}:{mongo_port}/"
    mongo_client = MongoClient(mongo_uri)
    mongo_db = mongo_client.medinote_db
    mongo_collection = mongo_db.patient_notes

    # Clear existing data to avoid duplicates on re-run
    mongo_collection.delete_many({})

    file_path = "data/patient_notes.json"
    with open(file_path, 'r') as f:
        for line in f:
            try:
                record = json.loads(line.strip())
                mongo_collection.insert_one(record)
                print(f"Inserted record for patient_id: {record.get('patient_id')}")
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e} in line: {line.strip()}")

    mongo_client.close()
    print("Data ingestion to MongoDB complete.")

if __name__ == "__main__":
    ingest_to_mongodb()