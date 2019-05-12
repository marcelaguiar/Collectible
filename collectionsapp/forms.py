from collectionsapp import models
from django import forms
from taggit.managers import TaggableManager


class CollectionForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Name',
    }))

    type = forms.ModelChoiceField(queryset=models.CollectionType.objects.all(),
                                  widget=forms.Select(attrs={'class': 'form-control'}), required=True)

    # def clean(self):
    #
    #     cleaned_data = super().clean()
    #     collection_name = cleaned_data.get("name")
    #     collection_type = cleaned_data.get("type")
    #
    #     if collection_name and collection_type:
    #         # Only do something if both fields are valid so far.
    #         if Collection.objects.filter(name=collection_name, type=collection_type).count() > 0:
    #             raise forms.ValidationError("You already own a collection with that name!")


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
    company = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Company',
    }))
    brand = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Brand',
    }))
    product = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Product',
    }))
    variety = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Variety',
    }))

    beverage_type = forms.ChoiceField()
    text = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Text',
    }))
    underside = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Underside',
    }))
    date_acquired = forms.DateField()
    method_acquired = forms.IntegerField()
    available_for_trade = forms.BooleanField()
    image = forms.ImageField()
    number_in_collection = forms.IntegerField()
    tags = TaggableManager()
    description = forms.CharField(max_length=512, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Description',
    }))
    collection = forms.ModelChoiceField(queryset=models.Collection.objects.all(),
                                        widget=forms.Select(attrs={'class': 'form-control'}), required=True)


#  TODO: Is this class even used?
class TempForm(forms.ModelForm):
    class Meta:
        model = models.CollectionType
        fields = ['name']
        widgets = {
            'name': forms.TextInput()
        }
