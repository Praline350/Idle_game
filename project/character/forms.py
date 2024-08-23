from django import forms
from .models import Character, Trailer

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ['name', 'age', 'sex']  # Inclut les champs nécessaires

class TrailerForm(forms.ModelForm):
    class Meta:
        model = Trailer
        fields = ['name'] 