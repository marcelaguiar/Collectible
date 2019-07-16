from collectionsapp.forms import CollectionTypeForm, CollectionForm, BottleCapForm
from collectionsapp.models import BeverageType, BottleCap, CollectionType, Collection, CollectionItem, User,\
    CollectionItemImage, CollectionItemImageThumbnail
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import Error
from django.db.models import fields
from django.db.models.fields import files
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from io import BytesIO
from PIL import Image
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
    if Collection.objects.get(id=collection_id).owner != request.user:
        return error(request, "You cannot add to other people's collections.")

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
            context = {
                'collectionForm': form,
                'collection_id': collection_id
            }
            return render(request, 'collectionsapp/add_to_collection.html', context)
    else:
        collection_item_form = BottleCapForm(initial={'collection': collection_id})

        context = {
            'collectionForm': collection_item_form,
            'collection_id': collection_id
        }
        return render(request, 'collectionsapp/add_to_collection.html', context)


def home(request):
    context = {
        'items': CollectionItemImageThumbnail.objects.filter(order_in_collection=1)
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


def explore_collection(request, collection_id, view):

    collection = Collection.objects.get(id=collection_id)
    images = None

    if view == 'image':
        images = CollectionItemImageThumbnail.objects.filter(
            order_in_collection=1,
            collection_item__collection=collection
        )

    context = {
        'collection_name': collection.name,
        'collection_id': collection_id,
        'is_owner': collection.created_by_id == request.user.id,
        'images': images,
        'view': view
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
    collection_item_image_formset = modelformset_factory(
        model=CollectionItemImage,
        fields=('image', 'order_in_collection'),
        extra=1,
        max_num=5
    )

    if request.method == "POST":
        formset = collection_item_image_formset(
            request.POST,
            request.FILES,
            queryset=CollectionItemImage.objects.filter(collection_item_id=collection_item_id)
        )

        if formset.is_valid():
            submit_time = datetime.datetime.now()

            collection_item = BottleCap.objects.get(id=collection_item_id)

            for f in formset:
                new_image = CollectionItemImage(
                    created=submit_time,
                    modified=submit_time,
                    order_in_collection=f.cleaned_data['order_in_collection'],
                    image=f.cleaned_data['image'],
                    collection_item=collection_item,
                    created_by=request.user,
                    modified_by=request.user
                )

                # Save full-quality image
                new_image.save()

                im = Image.open(new_image.image.path)

                width, height = im.size

                square_edge_length = 150
                target_width = square_edge_length
                target_height = square_edge_length

                left = 0
                top = 0
                right = target_width
                bottom = target_height

                # get new dimensions to fit
                if width > height:
                    resize_ratio = target_height / height
                    new_width = int(width * resize_ratio)
                    new_height = target_height
                elif height > width:
                    resize_ratio = target_width / width
                    new_width = target_width
                    new_height = int(height * resize_ratio)
                else:
                    new_width = target_width
                    new_height = target_height

                # grow or shrink to new dimensions
                if width >= target_width and height >= target_height:
                    im.thumbnail([new_width, new_height], Image.ANTIALIAS)
                else:
                    im = im.resize((new_width, new_height))
                    print("resize happened: w: " + str(im.width) + " h: " + str(im.height))
                print("new_width: " + str(new_width))
                print("new_height: " + str(new_height))

                # crop
                if new_width > target_width:
                    left = (new_width - target_width)/2
                    right = left + target_width
                elif new_height > target_height:
                    top = (new_height - target_height)/2
                    bottom = top + target_height

                print(left, top, right, bottom)

                im = im.crop((left, top, right, bottom))

                buffer = BytesIO()
                im.save(fp=buffer, format='JPEG', quality=95)
                pillow_image = ContentFile(buffer.getvalue())

                thumbnail = CollectionItemImageThumbnail(
                    created=submit_time,
                    modified=submit_time,
                    order_in_collection=f.cleaned_data['order_in_collection'],
                    image=pillow_image,
                    collection_item=collection_item,
                    created_by=request.user,
                    modified_by=request.user
                )

                thumbnail.save()

                thumbnail.image.save(
                    new_image.image.name,
                    InMemoryUploadedFile(
                        pillow_image,
                        None,               # field_name
                        'my_image.jpg',     # file name
                        'image/jpeg',       # content_type
                        pillow_image.tell,  # size
                        None
                    )
                )

            return bottle_cap(request, collection_item_id)
        else:
            print(formset.errors)
    else:
        collection = BottleCap.objects.get(pk=collection_item_id).collection

        context = {
            'collection': collection,
            'imageUploadFormSet': collection_item_image_formset(queryset=CollectionItemImage.objects.none())
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


def delete_collection_item(request, collection_item_id):
    instance = BottleCap.objects.get(id=collection_item_id)
    related_images = CollectionItemImage.objects.filter(collection_item_id=instance.pk)
    related_thumbnails = CollectionItemImageThumbnail.objects.filter(collection_item_id=instance.pk)

    related_images.delete()
    related_thumbnails.delete()

    collection_id = instance.collection_id
    instance.delete()

    return explore_collection(request, collection_id, "image")


def search(request):
    criteria = request.GET.get('q')

    context = {
        'criteria': criteria if criteria is not None else ""
    }
    return render(request, 'collectionsapp/search.html', context)


def get_all_bottle_caps(request):
    data = BottleCap.objects.all().values('id', 'company', 'brand', 'product', 'variety', 'beverage_type',
                                          'date_acquired')

    return JsonResponse(list(data), safe=False)


def get_all_bottle_caps_by_collection(request, collection_id):
    data = BottleCap.objects.filter(collection_id=collection_id)\
        .values('id', 'company', 'brand', 'product', 'variety', 'beverage_type', 'date_acquired')

    return JsonResponse(list(data), safe=False)


def get_all_bottle_caps_with_primary_image(request):
    data = CollectionItemImage.objects.select_related(order_in_collection=1).values()

    data = data.values('id', 'company', 'brand', 'product', 'variety', 'beverage_type', 'date_acquired')

    return JsonResponse(list(data), safe=False)


def get_all_beverage_types(request):
    data = BeverageType.objects.all().values('id', 'name')

    return JsonResponse(list(data), safe=False)
