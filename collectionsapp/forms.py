from collectionsapp import models
from django import forms


class CollectionTypeForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
                'class' : 'form-control',
                'placeholder' : 'Name',
    }))


class TempForm(forms.ModelForm):
    class Meta:
        model = models.CollectionType
        fields = ['name']
        widgets = {
            'name' : forms.TextInput()
        }