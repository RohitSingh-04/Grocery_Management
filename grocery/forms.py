from django import forms
from .models import *

class TypeForm(forms.ModelForm):
    typename = forms.CharField(label="Type Name", max_length=100, required=True)
    class Meta:
        model = Type
        fields = ['typename']
        

class ProductForm(forms.ModelForm):
    item_type = forms.ModelChoiceField(queryset=Type.objects.all(), label="Type of Product")
    name = forms.CharField(label="Name of Product", required=True, widget=forms.TextInput(attrs={'placeholder': 'Nascafe Classic Coffee'}))
    price = forms.FloatField(min_value=0, label="price per item (in INR)", required=True, widget=forms.NumberInput(attrs={'placeholder': '250.50'}))
    class Meta:
        model = Product
        fields = '__all__'

class RequestsForm(forms.ModelForm):
    item_type = forms.ModelChoiceField(queryset=Type.objects.all(), label="Type of Product")
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows':7, 'cols':50, 'placeholder':'comments...'}))
    class Meta:
        model = Requests
        fields = ['item_type', 'comment']
