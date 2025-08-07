import os
import json
from pymongo import MongoClient
from clickhouse_connect import get_client
from transformers import pipeline

# Initialize Hugging Face pipelines
# Using smaller, general-purpose models for demonstration
# For production, consider more specialized or larger models
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")
ner_recognizer = pipeline("token-classification", model="NeuronZero/MED-NER", aggregation_strategy='simple')

def enrich_and_store_data():
    # MongoDB Connection
    mongo_host = "localhost"
    mongo_port = os.getenv("MONGO_PORT", "27017")
    mongo_uri = f"mongodb://{mongo_host}:{mongo_port}/"
    mongo_client = MongoClient(mongo_uri)
    mongo_db = mongo_client.medinote_db
    mongo_collection = mongo_db.patient_notes

    # ClickHouse Connection
    clickhouse_host = "localhost"
    clickhouse_port = os.getenv("CLICKHOUSE_PORT", "8123")
    clickhouse_user = os.getenv("CLICKHOUSE_USER", "default")
    clickhouse_password = os.getenv("CLICKHOUSE_PASSWORD", "password")

    # Ensure ClickHouse port is an integer
    try:
        ch_port = int(clickhouse_port)
    except ValueError:
        print(f"Error: Invalid ClickHouse port '{clickhouse_port}'. Using default 8123.")
        ch_port = 8123

    clickhouse_client = get_client(
        host=clickhouse_host,
        port=ch_port,
        username=clickhouse_user,
        password=clickhouse_password
    )

    # Create ClickHouse table if it doesn't exist
    # This table will store the enriched data
    clickhouse_client.command("DROP TABLE IF EXISTS enriched_patient_notes")
    clickhouse_client.command("""
        CREATE TABLE IF NOT EXISTS enriched_patient_notes (
            patient_id String,
            original_note String,
            summary String,
            ner_entities String
        ) ENGINE = MergeTree()
        ORDER BY patient_id
    """)

    print("ClickHouse table 'enriched_patient_notes' ensured.")

    # Process data from MongoDB
    for record in mongo_collection.find():
        patient_id = record.get("patient_id")
        original_note = record.get("note")

        if not original_note:
            continue

        # Perform summarization
        summary_result = summarizer(original_note, max_length=100, min_length=30, do_sample=False)
        summary = summary_result[0]['summary_text']

        # Perform NER
        ner_result = ner_recognizer(original_note)
        # Extract only the entity, word, and score for simplicity
        ner_entities = json.dumps([{"entity": ent['entity_group'], "word": ent['word'], "score": float(ent['score'])} for ent in ner_result])

        # Prepare data for ClickHouse (as a list of values in correct order)
        enriched_data_row = [
            patient_id,
            original_note,
            summary,
            ner_entities
        ]

        # Insert into ClickHouse
        clickhouse_client.insert('enriched_patient_notes', [enriched_data_row])
        print(f"Enriched and stored data for patient_id: {patient_id}")

    mongo_client.close()
    clickhouse_client.close()
    print("Data enrichment and storage complete.")

if __name__ == "__main__":
    enrich_and_store_data()