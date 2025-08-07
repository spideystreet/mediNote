-- models/my_first_dbt_model.sql

SELECT
    patient_id,
    original_note,
    summary,
    ner_entities
FROM
    default.enriched_patient_notes
