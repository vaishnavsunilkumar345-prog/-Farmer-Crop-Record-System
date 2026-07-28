from django.db import models

class Crop(models.Model):
    crop_name = models.CharField(max_length=200)
    farmer_name = models.CharField(max_length=200)
    season = models.CharField(max_length=100)
    price = models.CharField(max_length=100)

    def __str__(self):
        return self.crop_name
