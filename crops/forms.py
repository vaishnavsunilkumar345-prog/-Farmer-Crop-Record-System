from django import forms
from .models import Crop

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['crop_name', 'farmer_name', 'season', 'price']
        widgets = {
            'crop_name': forms.TextInput(attrs={'class': 'input', 'id': 'id_crop_name'}),
            'farmer_name': forms.TextInput(attrs={'class': 'input', 'id': 'id_farmer_name'}),
            'season': forms.TextInput(attrs={'class': 'input', 'id': 'id_season'}),
            'price': forms.TextInput(attrs={'class': 'input', 'id': 'id_price'}),
        }
