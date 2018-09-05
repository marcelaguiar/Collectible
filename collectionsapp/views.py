from collectionsapp.forms import CollectionTypeForm, CollectionForm
from collectionsapp.models import BottleCap, CollectionType, Collection
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.db import Error
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
    context = {
        'collectionTypeForm': CollectionTypeForm
    }
    return render(request, 'collectionsapp/site_management.html', context)


@require_POST
def create_collection_type(request):
    form = CollectionTypeForm(request.POST)

    if form.is_valid():
        name = request.POST['name']
        render_page_name = request.POST['render_page_name']
        created_by = request.user
        modified_by = request.user
        new_collection_type = CollectionType(name=name, render_page_name=render_page_name, created_by=created_by,
                                             modified_by=modified_by)
        new_collection_type.save()

    return redirect('collection_types')


def bottle_cap_item(request, item_id):

    fields = []
    bottle_cap = BottleCap.objects.get(id=item_id)
    collection = bottle_cap.collection

    excluded_fields = [
        'created',
        'modified',
        'id',
        'image',
        'collection_id'
    ]

    for field in BottleCap._meta.get_fields():
        if field.name in excluded_fields:
            continue
        field_verbose_name = BottleCap._meta.get_field(field.name).verbose_name
        field_value = getattr(bottle_cap, field.name)

        fields.append({'attr': field_verbose_name, 'value': field_value})

    context = {
        'bottleCap': bottle_cap,
        'rows': fields,
        'itemsInCollection': BottleCap.objects.filter(collection=collection).count(),
        'username': 'test',
        'collectionName': Collection.objects.get(id=collection.pk).name
    }

    return render(request, 'collectionsapp/bottle_cap_item.html', context)


def my_collections(request):
    is_empty = True
    collection_query_set = Collection.objects.filter(owner=request.user)

    if collection_query_set.count() > 0:
        is_empty = False

    context = {
        'isEmpty': is_empty,
        'usersCollections': collection_query_set
    }
    return render(request, 'collectionsapp/my_collections.html', context)


def start_collection(request):
    collection_form = CollectionForm
    users_collections = Collection.objects.filter(owner=request.user)
    context = {
        'usersCollections': users_collections,
        'collectionForm': collection_form
    }
    return render(request, 'collectionsapp/start_collection.html', context)


@require_POST
def create_collection(request):
    form = CollectionForm(request.POST)

    if form.is_valid():
        name = request.POST['name']
        collection_type_id = request.POST['collection_type']

        # If user decides to not enter a name, we generate a name for them
        if not name:
            name = CollectionType.objects.get(id=collection_type_id).name + ' collection'

        owner = request.user
        created_by = request.user
        modified_by = request.user
        new_collection = Collection(name=name, collection_type_id=collection_type_id, owner=owner,
                                    created_by=created_by, modified_by=modified_by)
        try:
            new_collection.save()
            messages.add_message(request, messages.SUCCESS, name + ' collection created')
        except Error:
            messages.add_message(request, messages.ERROR, name + ' collection failed to create')

    return redirect('my_collections')


def explore_collection(request, collection_id):
    BOTTLE_CAPS = 'Bottle Caps'

    collection = Collection.objects.get(id=collection_id)

    if collection.collection_type_id == CollectionType.objects.get(name=BOTTLE_CAPS).pk:
        collection_items = BottleCap.objects.filter(collection_id=collection_id)
    else:
        collection_items = BottleCap.objects.filter(collection_id=collection_id)

    context = {
        'collection': collection_items
    }
    return render(request, 'collectionsapp/explore_collection.html', context)


def explore_collection_type(request, item_id):
    context = {
    }
    return render(request, 'collectionsapp/explore_collection_type.html', context)


def add_new_collection_item(request):
    collections = Collection.objects.filter(owner=request.user).order_by('name')
    collections_list = []
    collection_dict = {}

    for collection in collections:
        collection_dict['id'] = collection.pk
        collection_dict['url'] = collection.pk  # instead of this use corresponding form type
        collection_dict['name'] = collection.name
        collections_list.append(collection_dict)

    context = {
        'collections': collections_list
    }
    return render(request, 'collectionsapp/add_new_collection_item.html', context)
