from django import forms
from .models import Crop

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['crop_name', 'farmer_name', 'season', 'price']
        widgets = {
            'crop_name': forms.TextInput(attrs={'class': 'input', 'id': 'id_crop_name', 'placeholder': 'e.g. Basmati rice'}),
            'farmer_name': forms.TextInput(attrs={'class': 'input', 'id': 'id_farmer_name', 'placeholder': 'e.g. Ramesh Kumar'}),
            'season': forms.TextInput(attrs={'class': 'input', 'id': 'id_season', 'placeholder': 'e.g. Kharif 2026'}),
            'price': forms.TextInput(attrs={'class': 'input', 'id': 'id_price', 'placeholder': 'e.g. 2400 per quintal'}),
        }
