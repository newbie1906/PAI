from django import forms
from .models import Grzyby

class GrzybyForm(forms.ModelForm):
    class Meta:
        model = Grzyby
        fields = ['nameOfShroom', 'descriptionOfShroom', 'picker', 'weightOfShroom']