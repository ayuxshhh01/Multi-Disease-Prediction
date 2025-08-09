from django.urls import path
from . import views


urlpatterns = [
     path('predict/', views.predict_disease, name='predict_disease'),
    path('', views.home, name='home'),
     path('', views.home, name='home'),
     path("chatbot", views.chatbot, name="chatbot"),

    
]
