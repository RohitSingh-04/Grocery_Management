from django import forms
from .models import *

class TypeForm(forms.ModelForm):
    typename = forms.CharField(label="Type Name", max_length=100, required=True, widget=forms.TextInput(attrs = {'placeholder': 'Coffee', 'class':'form-control mt-2'}))
    class Meta:
        model = Type
        fields = ['typename']

class ProductForm(forms.ModelForm):
    item_type = forms.ModelChoiceField(queryset=Type.objects.all(), label="Type of Product")
    name = forms.CharField(label="Name of Product", required=True, widget=forms.TextInput(attrs={'placeholder': 'Nascafe Classic Coffee', 'class':'form-control mt-2'}))
    price = forms.FloatField(min_value=0, label="price per item (in INR)", required=True, widget=forms.NumberInput(attrs={'placeholder': '250.50', 'class':'form-control mt-2'}))
    class Meta:
        model = Product
        fields = '__all__'
    def __init__(self, *args, **kwargs) -> None:
        super(ProductForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['id'] = 'formGroupExampleInput'

class RequestsForm(forms.ModelForm):
    item_type = forms.ModelChoiceField(queryset=Type.objects.all(), label="Type of Product")
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows':7, 'cols':50, 'placeholder':'comments...'}))
    class Meta:
        model = Requests
        fields = ['item_type', 'comment']
    def __init__(self, *args, **kwargs) -> None:
        super(RequestsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['id'] = 'formGroupExampleInput'

class TypeDashForm(forms.ModelForm):
    typename = forms.ModelChoiceField(queryset=Type.objects.all(), label="Select a type of product")
    class Meta:
        model = Type
        fields = '__all__'
    def __init__(self, *args, **kwargs) -> None:
        super(TypeDashForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['id'] = 'formGroupExampleInput'