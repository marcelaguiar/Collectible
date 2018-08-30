from collectionsapp.forms import CollectionTypeForm
from collectionsapp.models import CollectionType, BottleCap
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST


def home(request):
    return render(request, 'collectionsapp/home.html')


def collection_types(request):
    all_collection_types = {'all_collection_types': CollectionType.objects.all()}
    return render(request, 'collectionsapp/collection_types.html', all_collection_types)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'registration/signup.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse(home))


def site_management(request):
    collection_type_form = CollectionTypeForm
    return render(request, 'collectionsapp/site_management.html', {'CollectionTypeForm': collection_type_form})


@require_POST
def create_collection_type(request):
    form = CollectionTypeForm(request.POST)

    if form.is_valid():
        new_collection_type = CollectionType(name=request.POST['name'])
        new_collection_type.save()

    return redirect('collection_types')


def bottle_cap_item(request, item_id):

    bottle_cap = BottleCap.objects.get(id=item_id)

    fields = []

    for field in BottleCap._meta.get_fields():
        field_verbose_name = BottleCap._meta.get_field(field.name).verbose_name
        field_value = getattr(bottle_cap, field.name)

        fields.append({'attr': field_verbose_name, 'value': field_value})

    context = {
        'bottleCap': BottleCap.objects.get(id=item_id),
        'fieldNames': [field.verbose_name for field in BottleCap._meta.get_fields()],
        'rows': fields
    }

    return render(request, 'collectionsapp/bottle_cap_item.html', context)
