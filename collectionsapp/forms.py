from collectionsapp import models
from django import forms


class CollectionForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name',
    }))

    type = forms.ModelChoiceField(queryset=models.CollectionType.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}), required=True)


class CollectionTypeForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name',
    }))
    render_page_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Render page name (ex: bottle_cap_item)',
    }))


class BottleCapForm(forms.Form):
    company = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Company',
    }))
    brand = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Brand',
    }))
    product = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Product',
    }))
    variety = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Variety',
    }))
    beverage_type = forms.ModelChoiceField(queryset=models.BeverageType.objects.all(),
                                           widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    text = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Text',
    }))
    underside = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Underside',
    }))
    date_acquired = forms.DateField(required=False)
    method_acquired = forms.ModelChoiceField(queryset=models.MethodAcquired.objects.all(),
                                             widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    available_for_trade = forms.BooleanField(required=False)
    tags = forms.CharField(max_length=512, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'ex: star, 1776, liberty',
    }))
    description = forms.CharField(max_length=512, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Description',
    }))
    collection = forms.ModelChoiceField(queryset=models.Collection.objects.filter(),
                                        widget=forms.Select(attrs={'class': 'form-control'}), required=True)


class CollectionItemImageForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput())
    order_in_collection = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={
        'class': 'form-control'
    }))

