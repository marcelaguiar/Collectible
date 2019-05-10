from collectionsapp.forms import CollectionTypeForm, CollectionForm, BottleCapForm
from collectionsapp.models import BottleCap, CollectionType, Collection, CollectionItem, User, CollectionItemImage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import Error
from django.db.models import fields
from django.db.models.fields import files
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from taggit.managers import TaggableManager


class FriendlyDataTypes:
    INT = 'number'
    BOOL = 't/f (checkbox)'
    FLOAT = 'decimal'
    CHAR = 'text'
    DATE = 'date'
    DATETIME = 'date + time'
    IMAGE = 'image'
    TAG = 'tagging feature'


def home(request):
    context = {
        'items': CollectionItemImage.objects.filter(order_in_collection=1)
    }
    return render(request, 'collectionsapp/home.html', context)


def collection_types(request):
    context = {
        'all_collection_types': CollectionType.objects.all().order_by('name')
    }
    return render(request, 'collectionsapp/collection_types.html', context)


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

    # TODO: Check that new collection type is unique
    if form.is_valid():
        name = request.POST['name']
        render_page_name = request.POST['render_page_name']
        created_by = request.user
        modified_by = request.user
        new_collection_type = CollectionType(name=name, render_page_name=render_page_name, created_by=created_by,
                                             modified_by=modified_by)
        new_collection_type.save()

    return redirect('collection_types')


def bottle_cap(request, item_id):
    columns = []
    bottle_cap = BottleCap.objects.get(id=item_id)

    collection = bottle_cap.collection

    excluded_fields = [
        'ID',
        'Modified',
        'Modified By',
        'Created',
        'Created By',
        'Collection ID',
        'Tags',
        'tagged items'
    ]

    # TODO: fix the method of getting field values
    for field in BottleCap._meta.get_fields():
        try:
            if field.verbose_name in excluded_fields:
                continue

            field_verbose_name = BottleCap._meta.get_field(field.name).verbose_name
            field_value = getattr(bottle_cap, field.name)
            print(str(field_verbose_name) + '\t' + str(field_value))
            columns.append({'attr': field_verbose_name, 'value': field_value})
        except AttributeError:
            print("An exception occurred......")
            continue

    context = {
        'bottle_cap': bottle_cap,
        'rows': columns,
        'itemsInCollection': BottleCap.objects.filter(collection=collection).count(),
        'collectionOwner': collection.created_by,
        'collectionName': Collection.objects.get(id=collection.pk).name,
        'collectionTypeName': collection.collection_type.name,
        'tags': bottle_cap.tags.all(),
        'imageSet': CollectionItemImage.objects.filter(collection_item=bottle_cap).order_by('order_in_collection')
    }

    return render(request, 'collectionsapp/bottle_cap.html', context)


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


@login_required
def start_collection(request):
    collection_form = CollectionForm
    context = {
        'collectionForm': collection_form
    }
    return render(request, 'collectionsapp/start_collection.html', context)


@require_POST
def select_fieldset(request):
    form = CollectionForm(request.POST)

    if not form.is_valid():
        pass  # TODO: GO back to previous page

    collection_name = request.POST['collection_name']
    collection_type_id = request.POST['collection_type']

    request.session['collection_name'] = collection_name
    request.session['collection_type_id'] = collection_type_id

    context = {
        'collectionType': CollectionType.objects.get(id=collection_type_id),
        'collectionName': collection_name
    }
    return render(request, 'collectionsapp/select_fieldset.html', context)


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
    bottle_caps = 'Bottle cap'

    collection = Collection.objects.get(id=collection_id)

    if collection.collection_type_id == CollectionType.objects.get(name=bottle_caps).pk:
        collection_items = BottleCap.objects.filter(collection_id=collection_id)
        display_form = 'bottle_cap'
    else:
        collection_items = BottleCap.objects.filter(collection_id=collection_id)
        display_form = 'item'

    context = {
        'collection_name': collection.name,
        'collection_items': collection_items,
        'collection_id': collection_id,
        'display_form': display_form,
        'is_owner': collection.created_by_id == request.user.id
    }
    return render(request, 'collectionsapp/explore_collection.html', context)


def explore_collection_type(request, collection_type_id):

    collections = Collection.objects.filter(collection_type_id=collection_type_id)

    context = {
        'collection_type': CollectionType.objects.get(id=collection_type_id),
        'collections': collections
    }
    return render(request, 'collectionsapp/explore_collection_type.html', context)


@login_required
def select_collection(request):
    # TODO: Check that the user is logged in
    collections_list = []

    for collection in Collection.objects.filter(owner=request.user).order_by('name'):
        collection_dict = {
            'id': collection.id,
            'name': collection.name
        }
        collections_list.append(collection_dict)

    context = {
        'collections': collections_list
    }

    return render(request, 'collectionsapp/select_collection.html', context)


def input_item_details(request, collection_id):
    # TODO: Check that the user is logged in
    collection_type = Collection.objects.get(id=collection_id).collection_type

    collection_form = get_item_input_form(collection_type)

    context = {
        'collectionForm': collection_form
    }
    return render(request, 'collectionsapp/input_item_details.html', context)


def get_item_input_form(collection_type):
    switcher = {
        'Bottle Caps': BottleCapForm,
    }
    return switcher.get(collection_type.name, "Invalid collection")


def create_item(request):
    context = {}
    return render(request, 'collectionsapp/home.html', context)


def select_existing_fieldset(request):
    context = {
    }
    return render(request, 'collectionsapp/select_existing_fieldset.html', context)


def design_fieldset(request):
    collection_type = CollectionType.objects.get(id=request.session.get('collection_type_id'))
    collection_name = request.session.get('collection_name')
    base_fields = []

    excluded_fields = [
        'Created',
        'Created By',
        'Modified',
        'Modified By',
        'Collection ID'
    ]

    i = 1
    for field in CollectionItem._meta.get_fields():
        if field.verbose_name in excluded_fields:
            continue

        base_field_dict = {
            'index': i,
            'verbose_name': field.verbose_name,
            'type': get_friendly_type(field)
        }

        base_fields.append(base_field_dict)
        i = i + 1

    context = {
        'collectionType': collection_type,
        'collectionName': collection_name,
        'baseFields': base_fields
    }
    return render(request, 'collectionsapp/design_fieldset.html', context)


def get_friendly_type(field):
    switch_dict = {
        fields.BooleanField: FriendlyDataTypes.BOOL,
        fields.IntegerField: FriendlyDataTypes.INT,
        fields.FloatField: FriendlyDataTypes.FLOAT,
        fields.CharField: FriendlyDataTypes.CHAR,
        fields.DateField: FriendlyDataTypes.DATE,
        fields.DateTimeField: FriendlyDataTypes.DATETIME,
        files.ImageField: FriendlyDataTypes.IMAGE,
        TaggableManager: FriendlyDataTypes.TAG
    }

    return switch_dict.get(type(field), '???')


def profile(request, user_id):
    target_user = User.objects.get(id=user_id)

    context = {
        'target_user': target_user
    }
    return render(request, 'collectionsapp/profile.html', context)


def tag_search_collection(request, collection_id, slug):

    collection_type_id = Collection.objects.get(id=collection_id).collection_type_id

    context = {
        'search_criteria': slug,
        'collection_id': collection_id,
        'collection_type_id': collection_type_id,
        'search_results': BottleCap.objects.filter(
            tags__slug__exact=slug,
            collection_id=collection_id)
    }

    return render(request, 'collectionsapp/tag_search_collection.html', context)


def tag_search_collection_type(request, collection_id, slug):

    collection_type_id = Collection.objects.get(id=collection_id).collection_type_id

    context = {
        'search_criteria': slug,
        'collection_id': collection_id,
        'collection_type_id': collection_type_id,
        'search_results': BottleCap.objects.filter(
            tags__slug__exact=slug,
            collection__collection_type_id=collection_type_id)
    }

    return render(request, 'collectionsapp/tag_search_collection_type.html', context)


def tag_search_all_collection_types(request, collection_id, slug):

    collection_type_id = Collection.objects.get(id=collection_id).collection_type_id

    context = {
        'search_criteria': slug,
        'collection_id': collection_id,
        'collection_type_id': collection_type_id,
        'search_results': BottleCap.objects.filter(
            tags__slug__exact=slug,
            collection__collection_type_id=collection_type_id)
    }

    return render(request, 'collectionsapp/tag_search_all_collection_types.html', context)
