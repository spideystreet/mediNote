import json

notes = [
    {
        "patient_id": "101",
        "note": "Patient John Doe, a 45-year-old male, presented to the emergency room on August 5, 2025, with severe abdominal pain, nausea, and vomiting. He reported the pain started suddenly after a heavy meal. Physical examination revealed tenderness in the right lower quadrant. Blood tests showed elevated white blood cell count. Suspected appendicitis. Dr. Smith ordered a CT scan for further evaluation. Patient has a history of hypertension and takes Lisinopril 10mg daily. No known drug allergies. Family history includes diabetes on his mother's side."
    },
    {
        "patient_id": "102",
        "note": "Patient Jane Smith, a 62-year-old female, attended her annual cardiology check-up on August 6, 2025. She has a history of coronary artery disease and underwent a stent placement in 2020. Current medications include Aspirin 81mg, Atorvastatin 20mg, and Metoprolol 50mg. ECG showed normal sinus rhythm. Blood pressure was 128/78 mmHg. Patient reports occasional mild chest discomfort during strenuous exercise but denies shortness of breath at rest. Dr. Brown advised continuing current medications and scheduled a stress test for next month. Advised to maintain a low-sodium diet."
    },
    {
        "patient_id": "103",
        "note": "Patient Michael Johnson, a 30-year-old male, visited the clinic for a follow-up on his asthma. He reports using his albuterol inhaler 3-4 times a week, which is an increase from his last visit. He experiences wheezing primarily at night and during exercise. Peak flow readings are consistently below his personal best. Dr. Davis reviewed his inhaler technique and prescribed a new inhaled corticosteroid, Fluticasone, to be used twice daily. Advised to avoid known triggers like dust and pet dander. Scheduled a follow-up in 4 weeks to assess control."
    },
    {
        "patient_id": "104",
        "note": "Patient Emily White, a 28-year-old female, presented with symptoms of a urinary tract infection (UTI), including dysuria, frequency, and urgency, starting 2 days ago. Urine dipstick was positive for leukocytes and nitrites. No fever or flank pain reported. Patient denies any recent sexual activity. Prescribed a 3-day course of Trimethoprim-sulfamethoxazole. Advised to drink plenty of fluids and return if symptoms worsen or do not improve within 48 hours. No significant past medical history."
    }
]

with open("data/patient_notes.json", "w") as f:
    for note in notes:
        f.write(json.dumps(note) + "\n")
