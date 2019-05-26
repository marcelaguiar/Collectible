from collectionsapp.forms import CollectionTypeForm, CollectionForm, BottleCapForm
from collectionsapp.models import BottleCap, CollectionType, Collection, CollectionItem, User, CollectionItemImage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import Error
from django.db.models import fields
from django.db.models.fields import files
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from taggit.managers import TaggableManager
import datetime


class FriendlyDataTypes:
    INT = 'number'
    BOOL = 't/f (checkbox)'
    FLOAT = 'decimal'
    CHAR = 'text'
    DATE = 'date'
    DATETIME = 'date + time'
    IMAGE = 'image'
    TAG = 'tagging feature'


@login_required
def add_to_collection(request, collection_id):
    if request.method == "POST":
        form = BottleCapForm(request.POST)

        if form.is_valid():
            new_bottle_cap = form.save(commit=False)
            new_bottle_cap.created_by = request.user
            new_bottle_cap.modified_by = request.user

            new_bottle_cap.save()

            form.save_m2m()

            return bottle_cap(request, new_bottle_cap.pk)
    else:
        collection_item_form = BottleCapForm(initial={'collection': collection_id})

        context = {
            'collectionForm': collection_item_form,
            'collection_id': collection_id
        }
        return render(request, 'collectionsapp/add_to_collection.html', context)


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
        created_by = request.user
        modified_by = request.user
        new_collection_type = CollectionType(name=name, created_by=created_by,
                                             modified_by=modified_by)
        new_collection_type.save()

    return redirect('collection_types')


def bottle_cap(request, item_id):

    bottle_cap_item = BottleCap.objects.get(id=item_id)

    collection = bottle_cap_item.collection

    context = {
        'bottle_cap': bottle_cap_item,
        'itemsInCollection': BottleCap.objects.filter(collection=collection).count(),
        'collectionOwner': collection.created_by,
        'collectionName': Collection.objects.get(id=collection.pk).name,
        'collectionTypeName': collection.type.name,
        'tags': bottle_cap_item.tags.all(),
        'imageSet': CollectionItemImage.objects.filter(collection_item=bottle_cap_item).order_by('order_in_collection'),
        'collection_item_id': item_id
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
    context = {
        'collectionForm': CollectionForm
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
        name = request.POST.get('name')
        collection_type_id = request.POST.get('type')
        owner = request.user
        created_by = request.user
        modified_by = request.user

        new_collection = Collection(name=name, type_id=collection_type_id, owner=owner,
                                    created_by=created_by, modified_by=modified_by)
        try:
            new_collection.save()
            messages.add_message(request, messages.SUCCESS, name + ' collection created')
            return redirect('explore_collection', collection_id=new_collection.pk)
        except Error:
            messages.add_message(request, messages.ERROR, name + ' collection failed to create')
            return redirect('my_collections')


def explore_collection(request, collection_id):
    collection = Collection.objects.get(id=collection_id)
    collection_items = BottleCap.objects.filter(collection_id=collection_id).order_by('-created')

    context = {
        'collection_name': collection.name,
        'collection_items': collection_items,
        'collection_id': collection_id,
        'is_owner': collection.created_by_id == request.user.id
    }
    return render(request, 'collectionsapp/explore_collection.html', context)


def explore_collection_type(request, collection_type_id):

    collection_type = CollectionType.objects.get(id=collection_type_id)
    collections = Collection.objects.filter(type__id=collection_type_id)

    context = {
        'collection_type': collection_type,
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

    collection_type_id = Collection.objects.get(id=collection_id).type.id

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

    collection_type_id = Collection.objects.get(id=collection_id).type.id

    context = {
        'search_criteria': slug,
        'collection_id': collection_id,
        'collection_type_id': collection_type_id,
        'search_results': BottleCap.objects.filter(
            tags__slug__exact=slug,
            collection__type_id=collection_type_id)
    }

    return render(request, 'collectionsapp/tag_search_collection_type.html', context)


def tag_search_all_collection_types(request, collection_id, slug):

    collection_type_id = Collection.objects.get(id=collection_id).type.id

    context = {
        'search_criteria': slug,
        'collection_id': collection_id,
        'collection_type_id': collection_type_id,
        'search_results': BottleCap.objects.filter(
            tags__slug__exact=slug,
            collection__type_id=collection_type_id)
    }

    return render(request, 'collectionsapp/tag_search_all_collection_types.html', context)


@login_required
def upload_image(request, collection_item_id):
    CollectionItemImageFormset = modelformset_factory(
        model=CollectionItemImage,
        fields=('image', 'order_in_collection'),
        extra=1,
        max_num=5
    )

    if request.method == "POST":
        formset = CollectionItemImageFormset(
            request.POST,
            request.FILES,
            queryset=CollectionItemImage.objects.filter(collection_item_id=collection_item_id)
        )

        if formset.is_valid():
            submit_time = datetime.datetime.now()

            for f in formset:
                new_image = CollectionItemImage(
                    created=submit_time,
                    modified=submit_time,
                    order_in_collection=f.cleaned_data['order_in_collection'],
                    image=f.cleaned_data['image'],
                    collection_item=BottleCap.objects.get(id=collection_item_id),
                    created_by=request.user,
                    modified_by=request.user
                )

                new_image.save()

            return bottle_cap(request, collection_item_id)
        else:
            print(formset.errors)
    else:
        collection = BottleCap.objects.get(pk=collection_item_id).collection

        context = {
            'collection': collection,
            'imageUploadFormSet': CollectionItemImageFormset(queryset=CollectionItemImage.objects.none())
        }

        return render(request, 'collectionsapp/upload_image.html', context)


@login_required
def edit_collection_item(request, collection_item_id):
    collection_item = get_object_or_404(BottleCap, pk=collection_item_id)

    if collection_item.collection.owner != request.user:
        return error(request, "You cannot edit other people's items.")

    if request.method == "POST":
        form = BottleCapForm(request.POST, instance=collection_item)

        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.modified_by = request.user
            form_data.created_by = collection_item.created_by

            form_data.save()

            form.save_m2m()

            return bottle_cap(request, form_data.pk)
    else:
        context = {
            'collectionForm': BottleCapForm(instance=collection_item),
            'collection_item_id': collection_item_id
        }
        return render(request, 'collectionsapp/edit_collection_item.html', context)


def error(request, description):
    context = {
        'description': description
    }
    return render(request, 'collectionsapp/error.html', context)
