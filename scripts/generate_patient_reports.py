import os
import json
from clickhouse_connect import get_client

# Configuration
CLICKHOUSE_HOST = "localhost"
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT", "8123")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "password")

OUTPUT_DIR = "reports"

def generate_patient_reports():
    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Connect to ClickHouse
    try:
        ch_port = int(CLICKHOUSE_PORT)
    except ValueError:
        print(f"Error: Invalid ClickHouse port '{CLICKHOUSE_PORT}'. Using default 8123.")
        ch_port = 8123

    client = get_client(
        host=CLICKHOUSE_HOST,
        port=ch_port,
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD
    )

    # Fetch data from enriched_patient_data view
    query = "SELECT patient_id, original_note, summary, ner_entities FROM default.enriched_patient_data"
    result = client.query(query)

    for row in result.result_rows:
        patient_id = row[0]
        original_note = row[1]
        summary = row[2]
        ner_entities_json = row[3]

        patient_dir = os.path.join(OUTPUT_DIR, f"patient_{patient_id}")
        os.makedirs(patient_dir, exist_ok=True)

        report_filepath = os.path.join(patient_dir, f"report_{patient_id}.md")

        with open(report_filepath, 'w', encoding='utf-8') as f:
            f.write(f"# Patient Report: {patient_id}\n\n")
            f.write(f"## Original Note\n\n")
            f.write(f"> {original_note}\n\n")
            f.write(f"## Summary\n\n")
            f.write(f"> {summary}\n\n")
            f.write(f"## Extracted Entities\n\n")

            try:
                entities = json.loads(ner_entities_json)
                if entities:
                    # Group entities by type for better readability
                    grouped_entities = {}
                    for ent in entities:
                        entity_type = ent.get('entity', 'UNKNOWN')
                        word = ent.get('word', '')
                        score = ent.get('score', 0.0)
                        if entity_type not in grouped_entities:
                            grouped_entities[entity_type] = []
                        grouped_entities[entity_type].append(f"- {word} (Score: {score:.2f})")

                    for entity_type, words in grouped_entities.items():
                        f.write(f"### {entity_type}\n\n")
                        for word_entry in words:
                            f.write(f"{word_entry}\n")
                        f.write("\n")
                else:
                    f.write("No entities extracted.\n")
            except json.JSONDecodeError:
                f.write(f"Error parsing NER entities JSON: {ner_entities_json}\n")

        print(f"Generated report for patient {patient_id} at {report_filepath}")

    client.close()
    print("Report generation complete.")

if __name__ == "__main__":
    generate_patient_reports()
