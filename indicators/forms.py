from django import forms
from .models import IndicatorData

class IndicatorDataForm(forms.ModelForm):
    class Meta:
        model = IndicatorData
        fields = ['indicator', 'month', 'year', 'value']
        widgets = {
            'indicator': forms.HiddenInput(),
            'month': forms.HiddenInput(),
            'year': forms.HiddenInput(),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
