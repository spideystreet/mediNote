import streamlit as st
import os
import json
from clickhouse_connect import get_client

# Configuration
CLICKHOUSE_HOST = "localhost"
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT", "8123")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "password")

@st.cache_resource
def get_clickhouse_client():
    try:
        ch_port = int(CLICKHOUSE_PORT)
    except ValueError:
        st.error(f"Error: Invalid ClickHouse port '{CLICKHOUSE_PORT}'. Using default 8123.")
        ch_port = 8123
    return get_client(
        host=CLICKHOUSE_HOST,
        port=ch_port,
        username=CLICKHOUSE_USER,
        password=CLICKHOUSE_PASSWORD
    )

client = get_clickhouse_client()

st.set_page_config(layout="wide", page_title="mediNote Data Explorer")
st.title("🩺 mediNote Data Explorer")

# Fetch all patient IDs
@st.cache_data
def get_patient_ids():
    query = "SELECT DISTINCT patient_id FROM default.enriched_patient_data ORDER BY patient_id"
    result = client.query(query)
    return [row[0] for row in result.result_rows]

patient_ids = get_patient_ids()

if not patient_ids:
    st.warning("No patient data found in ClickHouse. Please run the full pipeline first.")
else:
    selected_patient_id = st.sidebar.selectbox("Select a Patient ID", patient_ids)

    if selected_patient_id:
        # Fetch data for the selected patient
        query = f"SELECT original_note, ner_entities FROM default.enriched_patient_data WHERE patient_id = '{selected_patient_id}'"
        patient_data = client.query(query).result_rows[0]

        original_note = patient_data[0]
        ner_entities_json = patient_data[1]

        st.header(f"Patient ID: {selected_patient_id}")

        st.subheader("Original Note")
        st.markdown(f"> {original_note}")

        st.subheader("Extracted Entities")
        try:
            entities = json.loads(ner_entities_json)
            if entities:
                grouped_entities = {}
                entity_counts = {}
                for ent in entities:
                    entity_type = ent.get('entity', 'UNKNOWN')
                    word = ent.get('word', '')
                    score = ent.get('score', 0.0)
                    if entity_type not in grouped_entities:
                        grouped_entities[entity_type] = []
                    grouped_entities[entity_type].append(f"- **{word}** (Score: {score:.2f})")
                    entity_counts[entity_type] = entity_counts.get(entity_type, 0) + 1

                st.write("**Overview of Entity Counts:**")
                counts_display = ", ".join([f"{ent_type}: {count}" for ent_type, count in sorted(entity_counts.items())])
                st.write(counts_display)
                st.markdown("\n")

                for entity_type, words in sorted(grouped_entities.items()):
                    with st.expander(f"### {entity_type} ({entity_counts[entity_type]} entities)"):
                        # Join all word entries for this entity type into a single line
                        joined_words = ", ".join([entry.lstrip("- ") for entry in words])
                        st.markdown(joined_words)
            else:
                st.info("No entities extracted for this patient.")
        except json.JSONDecodeError:
            st.error(f"Error parsing NER entities JSON for this patient.")
