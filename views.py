from django.shortcuts import render,request
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

@csrf_exempt
def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        symptoms = request.POST.getlist('symptoms')
        location = request.POST.get('location')
        temperature = request.POST.get('temperature')
        humidity = request.POST.get('humidity')

        # For now just return back the same data (next step: ML model)
        return render(request, 'index.html', {
            'message': f"Received data for {name}. Symptoms: {', '.join(symptoms)}"
        })
    

    
    return render(request, 'index.html')
