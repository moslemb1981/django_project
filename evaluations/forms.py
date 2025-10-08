from django import forms
from .models import Evaluation

class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['employee', 'score', 'notes']    # مطمئن شو همین فیلدها در مدل هست

    def clean_score(self):
        s = self.cleaned_data.get('score')
        if s is None: return s
        if s < 0 or s > 100:
            raise forms.ValidationError("امتیاز باید بین 0 و 100 باشد.")
        return s
