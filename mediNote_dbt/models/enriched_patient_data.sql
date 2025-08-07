SELECT
    patient_id,
    original_note,
    ner_entities,
    -- Extract entity_group and word from the first element of the ner_entities array
    JSONExtractString(ner_entities, '$[0].entity_group') AS first_entity_group,
    JSONExtractString(ner_entities, '$[0].word') AS first_entity_word
FROM
    default.enriched_patient_notes