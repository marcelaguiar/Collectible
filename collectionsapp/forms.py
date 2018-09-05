from collectionsapp import models
from django import forms


class CollectionForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name',
    }))

    collection_type = forms.ModelChoiceField(queryset=models.CollectionType.objects.all(),
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


#  TODO: Is this class even used?
class TempForm(forms.ModelForm):
    class Meta:
        model = models.CollectionType
        fields = ['name']
        widgets = {
            'name': forms.TextInput()
        }
