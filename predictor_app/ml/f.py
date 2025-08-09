import pandas as pd
import random

# Expanded symptoms list
symptoms = [
    "fever", "cough", "headache", "fatigue", "nausea", "vomiting", "diarrhea", "shortness_of_breath",
    "chest_pain", "sore_throat", "runny_nose", "loss_of_smell", "loss_of_taste", "muscle_pain", "joint_pain",
    "rash", "itching", "redness", "swelling", "blisters", "dry_skin", "pale_skin", "yellow_skin",
    "blurred_vision", "dizziness", "fainting", "high_blood_sugar", "low_blood_sugar", "frequent_urination",
    "burning_urination", "abdominal_pain", "back_pain", "weight_loss", "weight_gain", "night_sweats",
    "chills", "confusion", "irritability", "anxiety", "depression", "swollen_lymph_nodes", "ear_pain", 
    "hearing_loss", "eye_pain", "sensitivity_to_light"
]

# Expanded diseases list
diseases = [
    "Common Cold", "Flu", "COVID-19", "Malaria", "Dengue", "Pneumonia", "Tuberculosis",
    "Diabetes", "Hypertension", "Heart Disease", "Asthma", "Allergy", "Skin Disease",
    "Conjunctivitis", "Otitis Media", "Migraine", "Anxiety Disorder", "Depression", "Food Poisoning", "Arthritis"
]

# Generate synthetic dataset
rows = []
for _ in range(1000):  # 1000 patient samples
    disease = random.choice(diseases)
    symptom_values = []
    
    # Assign symptoms based on disease relevance
    for symptom in symptoms:
        # Increase probability if symptom matches disease pattern
        if disease == "Common Cold":
            val = 1 if symptom in ["cough", "runny_nose", "sore_throat", "fever"] and random.random() < 0.8 else random.choices([0, 1], [0.9, 0.1])[0]
        elif disease == "Flu":
            val = 1 if symptom in ["fever", "cough", "muscle_pain", "fatigue"] and random.random() < 0.85 else random.choices([0, 1], [0.9, 0.1])[0]
        elif disease == "COVID-19":
            val = 1 if symptom in ["fever", "cough", "loss_of_smell", "shortness_of_breath"] and random.random() < 0.9 else random.choices([0, 1], [0.9, 0.1])[0]
        else:
            val = random.choices([0, 1], [0.85, 0.15])[0]
        symptom_values.append(val)
    
    rows.append(symptom_values + [disease])

# Create DataFrame
df = pd.DataFrame(rows, columns=symptoms + ["disease"])

# Save to CSV
df.to_csv("expanded_disease_dataset.csv", index=False)
print("Dataset created: expanded_disease_dataset.csv with", len(df), "rows and", len(df.columns)-1, "symptoms.")
