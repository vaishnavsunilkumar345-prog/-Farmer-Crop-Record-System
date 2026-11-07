from django.conf import settings
from django.db import models

class Crop(models.Model):
    crop_name = models.CharField(max_length=200)
    farmer_name = models.CharField(max_length=200)
    season = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name='crops')

    def __str__(self):
        return self.crop_name
