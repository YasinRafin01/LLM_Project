from django.db import models
from Hotel_info.models import Property  # Adjust if your Property model is in a different app

class PropertySummary(models.Model):
    property_id = models.OneToOneField(Property, on_delete=models.CASCADE, primary_key=True)
    summary = models.TextField()

    def __str__(self):
        return f"Summary for Property {self.property_id}"