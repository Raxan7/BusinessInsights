from django import forms


class BusinessInsightForm(forms.Form):
    # product_name = forms.CharField(label='Product Name', max_length=100)
    country = forms.CharField(label='Country Target', max_length=100)
