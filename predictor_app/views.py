import os
import json
import joblib
import requests
import numpy as np
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail

# -------------------- Load Models & Data --------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load once at the top
model = joblib.load(os.path.join(BASE_DIR, 'ml', 'model.pkl'))
symptom_list = joblib.load(os.path.join(BASE_DIR, 'ml', 'symptoms_list.pkl'))
label_encoder = joblib.load(os.path.join(BASE_DIR, 'ml', 'label_encoder.pkl'))


with open(os.path.join(BASE_DIR, 'ml', 'prescriptions.json'), 'r') as f:
    prescriptions = json.load(f)

CRITICAL_DISEASES = ["Heart Disease", "Stroke", "Sepsis", "Cancer", "Diabetes"]

# -------------------- Utilities --------------------
def send_sos_email(disease, probability, symptoms, user_info):
    subject = f"🚨 Emergency Alert: {disease} Detected ({probability}% Confidence)"
    message = (
        f"A case of {disease} was detected with {probability}% confidence.\n\n"
        f"Symptoms: {', '.join(symptoms)}\n\n"
        f"User Info:\n"
        f"Name: {user_info.get('name')}\n"
        f"Location: {user_info.get('location')}\n"
        f"Temperature: {user_info.get('temperature')}°C\n"
        f"Humidity: {user_info.get('humidity')}%\n\n"
        "Immediate medical attention may be required."
    )
    send_mail(subject, message, 'ayushdube596@gmail.com', ['ayushdube1316@icloud.com'])


def get_location_from_ip():
    try:
        response = requests.get("https://ipinfo.io/json")
        if response.status_code == 200:
            data = response.json()
            return data.get("city", "Unknown")
    except:
        return "Unknown"

# -------------------- API Endpoint --------------------
from .models import PredictionRecord


@csrf_exempt
def predict_disease(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        symptoms = data.get('symptoms', [])
        location = data.get('location', '')
        temperature = data.get('temperature', None)
        humidity = data.get('humidity', None)
        rainfall = data.get('rainfall', None)

        # Convert symptoms to binary vector in symptom_list order
        input_vector = [1 if symptom in symptoms else 0 for symptom in symptom_list]
        prediction = model.predict([input_vector])
        predicted_diseases = prediction.tolist()

        # Save to DB
        PredictionRecord.objects.create(
            symptoms=json.dumps(symptoms),
            predicted_diseases=json.dumps([prediction]),
            location=location,
            temperature=temperature,
            humidity=humidity,
            rainfall=rainfall
        )

        return JsonResponse({
            'predicted_diseases': [prediction]
        })

    return JsonResponse({'error': 'Invalid request method'}, status=400)
import re

@csrf_exempt
def chatbot(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "").lower()

        # Extract symptoms based on your symptom_list
        detected_symptoms = []
        for symptom in symptom_list:
            if symptom.lower().replace("_", " ") in user_message:
                detected_symptoms.append(symptom)

        if not detected_symptoms:
            return JsonResponse({"reply": "I couldn't detect any known symptoms. Could you rephrase?"})

        # Convert to vector & predict
        input_vector = [1 if s in detected_symptoms else 0 for s in symptom_list]
        import pandas as pd
        input_df = pd.DataFrame([input_vector], columns=symptom_list)

        proba = model.predict_proba(input_df)[0]
        top_index = proba.argmax()
        predicted_disease = label_encoder.inverse_transform([top_index])[0]
        probability = round(proba[top_index] * 100, 2)

        prescription = prescriptions.get(predicted_disease, "Please consult a doctor.")

        reply = (
            f"It seems you may have **{predicted_disease}** "
            f"({probability}% confidence). Recommended: {prescription}"
        )

        return JsonResponse({"reply": reply})

    return JsonResponse({"error": "Invalid method"}, status=400)


# -------------------- Web View --------------------
@csrf_exempt
def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        symptoms = request.POST.getlist('symptoms')

        location = request.POST.get('location') or get_location_from_ip()
        temperature = request.POST.get('temperature') or "32"
        humidity = request.POST.get('humidity') or "65"

        # Input vector
        input_vector = [1 if symptom in symptoms else 0 for symptom in symptom_list]
        import pandas as pd
        input_df = pd.DataFrame([input_vector], columns=symptom_list)

        # Probabilities
        proba = model.predict_proba(input_df)[0]
        top_indices = proba.argsort()[-3:][::-1]

        top_diseases = [
            {
                "name": label_encoder.inverse_transform([i])[0],
                "probability": round(proba[i] * 100, 2),
                "critical": label_encoder.inverse_transform([i])[0] in CRITICAL_DISEASES
            }
            for i in top_indices
        ]

        # Top disease
        prediction = top_diseases[0]["name"]
        prescription = prescriptions.get(prediction, "Please consult a doctor immediately.")

        # Send alert if critical
        if prediction in CRITICAL_DISEASES:
            send_sos_email(prediction, top_diseases[0]["probability"], symptoms, {
                'name': name,
                'location': location,
                'temperature': temperature,
                'humidity': humidity
            })

        return render(request, 'index.html', {
            'name': name,
            'location': location,
            'temperature': temperature,
            'humidity': humidity,
            'predicted_disease': prediction,
            'prescription': prescription,
            'top_diseases': top_diseases
        })

    return render(request, 'index.html')
