from django.contrib import admin
from .models import Crop

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('crop_name', 'farmer_name', 'season', 'price', 'owner')
    list_filter = ('season',)
    search_fields = ('crop_name', 'farmer_name', 'season')
