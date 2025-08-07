import json

notes = [
    {
        "patient_id": "123",
        "note": "Patient complains of a persistent cough and fever. Suspected case of bronchitis. Prescribed antibiotics and rest."
    },
    {
        "patient_id": "456",
        "note": "Annual check-up. Patient is in good health. Discussed diet and exercise. No issues to report."
    },
    {
        "patient_id": "789",
        "note": "Follow-up for hypertension. Blood pressure is stable. Continue with current medication. Next appointment in 3 months."
    }
]

with open("../data/patient_notes.json", "w") as f:
    for note in notes:
        f.write(json.dumps(note) + "\n")
