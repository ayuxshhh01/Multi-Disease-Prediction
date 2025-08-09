from django.db import models
from django.utils import timezone

class PredictionRecord(models.Model):
    symptoms = models.TextField()
    predicted_diseases = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=255, blank=True, null=True)  # optional
    temperature = models.FloatField(blank=True, null=True)
    humidity = models.FloatField(blank=True, null=True)
    rainfall = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Prediction at {self.timestamp}"
