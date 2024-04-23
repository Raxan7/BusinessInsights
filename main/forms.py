from django import forms
from .models import Sales


class BusinessInsightForm(forms.Form):
    url = forms.CharField(label='API Endpoint', max_length=100, initial="https://your/api/endpoint")
    # country = forms.CharField(label='Country Target', max_length=100)


class SalesDataForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = "__all__"

        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
        }
