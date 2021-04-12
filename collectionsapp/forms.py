from collectionsapp.models import Collection, CollectionType, BottleCap
from crispy_forms.helper import FormHelper
from datetime import date
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'type', 'description']

    def __init__(self, *args, **kwargs):
        super(CollectionForm, self).__init__(*args, **kwargs)

        # disable type on edit
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['type'].widget.attrs['disabled'] = True

        # Add placeholder text to fields
        self.fields['name'].widget.attrs.update({'placeholder': 'Name'})
        self.fields['type'].widget.attrs.update({'placeholder': 'Type'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Description'})


class CollectionEditForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(CollectionEditForm, self).__init__(*args, **kwargs)

        # Add placeholder text to fields
        self.fields['name'].widget.attrs.update({'placeholder': 'Name'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Description'})


class CollectionTypeForm(forms.ModelForm):
    class Meta:
        model: CollectionType
        fields = ['name']


class BottleCapForm(forms.ModelForm):
    class Meta:
        model = BottleCap
        fields = [
            'image',
            'company',
            'brand',
            'product',
            'variety',
            'beverage_type',
            'description',
            'region',
            'available_for_trade',
            'text',
            'underside',
            'tags'
        ]

    def __init__(self, *args, **kwargs):
        super(BottleCapForm, self).__init__(*args, **kwargs)

        # Add placeholder text to fields
        self.fields['image'].widget.attrs.update({'placeholder': 'Image'})
        self.fields['company'].widget.attrs.update({'placeholder': 'Company'})
        self.fields['brand'].widget.attrs.update({'placeholder': 'Brand'})
        self.fields['product'].widget.attrs.update({'placeholder': 'Product'})
        self.fields['variety'].widget.attrs.update({'placeholder': 'Variety'})
        self.fields['text'].widget.attrs.update({'placeholder': 'Text'})
        self.fields['region'].widget.attrs.update({'placeholder': 'Region'})
        self.fields['underside'].widget.attrs.update({'placeholder': 'Underside'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Description'})


'''class CollectionItemImageForm(forms.ModelForm):
    class Meta:
        model = CollectionItemImage
        fields = ['image', 'collection_item', 'order_in_collection']

    def __init__(self, *args, **kwargs):
        super(CollectionItemImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['collection_item'].widget.attrs.update({'class': 'form-control'})
        self.fields['order_in_collection'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Order'})'''


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AccountDeleteForm(forms.Form):
    username = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(AccountDeleteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False 
