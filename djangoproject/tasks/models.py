from django.db import models
from django.contrib.gis.db import models

class Task(models.Model):
    name = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Location(models.Model):
    name = models.CharField(max_length=255)
    coordinates = models.PointField()  # Geospatial field

    def __str__(self):
        return self.name
