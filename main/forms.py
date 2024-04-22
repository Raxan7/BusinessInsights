from django import forms
from .models import Sales


class BusinessInsightForm(forms.Form):
    # product_name = forms.CharField(label='Product Name', max_length=100)
    country = forms.CharField(label='Country Target', max_length=100)


class SalesDataForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = "__all__"

        widgets = {
            'date': forms.TextInput(attrs={'type': 'date'}),
        }
