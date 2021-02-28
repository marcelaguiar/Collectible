from collectionsapp.forms import CollectionTypeForm, CollectionForm, CollectionEditForm, BottleCapForm,\
    UserRegisterForm, AccountDeleteForm
from collectionsapp.helpers import delete_helper, image_helper
from collectionsapp.models import BottleCap, CollectionType, Collection, CollectionItem, User, SearchAction
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import Error
from django.db.models import fields, Count, Max
from django.db.models.fields import files
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from taggit.managers import TaggableManager
import datetime
import json
import os
import requests


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
    collection = Collection.objects.get(id=collection_id)

    if collection.owner != request.user:
        messages.warning(request, 'You cannot add to other people\'s collections.')
        return redirect('select_collection')

    if request.method == "POST":
        form = BottleCapForm(request.POST, request.FILES)

        if form.is_valid():
            collection_item = form.save(commit=False)
            uploaded_image = form.cleaned_data['image']
            pillow_image = image_helper.generate_thumbnail(uploaded_image)
            collection_item.created_by = request.user
            collection_item.modified_by = request.user
            collection_item.collection_id = collection_id

            collection_item.image_thumbnail.save(
                uploaded_image.name,
                InMemoryUploadedFile(
                    pillow_image,
                    None,               # field_name
                    'my_image.jpg',     # file name
                    'image/jpeg',       # content_type
                    pillow_image.tell,  # size
                    None
                )
            )

            collection_item.save()

            form.save_m2m()

            messages.success(request, 'Item added to collection.')
            return redirect('bottle_cap', item_id=collection_item.pk)
    else:
        form = BottleCapForm(initial={'collection': collection_id})

        context = {
            'form': form,
            'collection_id': collection_id
        }

        return render(request, 'collectionsapp/add_to_collection.html', context)


def home(request):
    context = {
        'items': BottleCap.objects.all().order_by('-created')[:settings.IMG_GRID_INIT_LOAD_QTY],
        'initial_load_quantity': settings.IMG_GRID_INIT_LOAD_QTY
    }
    return render(request, 'collectionsapp/home.html', context)


def get_n_thumbnails(request, start, end, collection_id):
    thumbnails = []

    if collection_id == 0:
        collection_items = BottleCap.objects.all().order_by('-created')[start:end]
    else:
        collection_items = BottleCap.objects.filter(collection_id=collection_id).order_by('-created')[start:end]

    for collection_item in collection_items:
        collection_item_url = reverse(viewname='bottle_cap', args=[collection_item.id])
        thumbnail_url = collection_item.image_thumbnail.url
        collection_item_name = str(collection_item)
        thumbnails.append(
            {
                "collection_item_url": collection_item_url,
                "image_url": thumbnail_url,
                "collection_item_name": collection_item_name
            }
        )

    return JsonResponse(thumbnails, safe=False)


def collection_types(request):
    context = {
        'all_collection_types': CollectionType.objects.all().order_by('name')
    }
    return render(request, 'collectionsapp/collection_types.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        captcha_response_token = request.POST.get("g-recaptcha-response")
        verification_url = "https://www.google.com/recaptcha/api/siteverify"
        secret_key = os.environ.get('reCAPTCHA_SECRET_KEY')

        payload = {
            "secret": secret_key,
            "response": captcha_response_token
        }

        cap_server_response = requests.post(url=verification_url, data=payload)
        cap_json = json.loads(cap_server_response.text)

        if cap_json["success"]:
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')

                messages.success(request, f'Account created for {username} and signed in!')

                user = authenticate(username=username, password=password)
                login(request, user)

                return redirect('home')
        else:
            messages.error(request, 'Invalid captcha. Try again.')
    else:
        form = UserRegisterForm()
    context = {
        'form': form,
        'recaptcha_site_key': os.environ.get('reCAPTCHA_SITE_KEY')
    }
    return render(request, 'registration/register.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse(home))


def site_management(request):
    context = {
        'collectionTypeForm': CollectionTypeForm
    }
    return render(request, 'collectionsapp/site_management.html', context)


def bottle_cap(request, item_id):
    bottle_cap_item = BottleCap.objects.get(id=item_id)
    collection = bottle_cap_item.collection

    context = {
        'bottle_cap': bottle_cap_item,
        'collectionOwner': collection.created_by,
        'collectionName': collection.name,
        'collectionTypeName': collection.type.name,
        'tags': bottle_cap_item.tags.all()
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
        'form': CollectionForm
    }
    return render(request, 'collectionsapp/start_collection.html', context)


def create_collection(request):
    form = CollectionForm(request.POST)

    if form.is_valid():
        name = request.POST.get('name')
        collection_type_id = request.POST.get('type')
        description = request.POST.get('description')
        owner = request.user
        created_by = request.user
        modified_by = request.user

        new_collection = Collection(
            name=name,
            type_id=collection_type_id,
            description=description,
            owner=owner,
            created_by=created_by,
            modified_by=modified_by
        )

        try:
            new_collection.save()
            messages.success(request, name + ' collection created')
            return redirect('explore_collection', collection_id=new_collection.pk, view='image')
        except Error:
            messages.error(request, name + ' collection failed to create')
            return redirect('my_collections')


def explore_collection(request, collection_id, view):
    collection = Collection.objects.get(id=collection_id)
    collection_items = None

    if view == 'image':
        collection_items = BottleCap.objects.filter(
            collection=collection
        ).order_by('-created')[:settings.IMG_GRID_INIT_LOAD_QTY]

    context = {
        'collection_name': collection.name,
        'collection_description': collection.description,
        'collection_id': collection.id,
        'has_description': bool(collection.description.strip()),
        'is_owner': collection.created_by_id == request.user.id,
        'collection_items': collection_items,
        'view': view,
        'initial_load_quantity': settings.IMG_GRID_INIT_LOAD_QTY
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


def collections(request):
    query = ''
    with open('collectionsapp/static/collectionsapp/sql/get_collections.sql', 'r') as file:
        query = file.read()

    collection_objects = BottleCap.objects.raw(query)

    context = {
        'collections': collection_objects,
        'collection_types': CollectionType.objects.all()
    }

    return render(request, 'collectionsapp/collections.html', context)


@login_required
def select_collection(request):
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


def tag_search(request, collection_id, slug):
    collection = Collection.objects.get(id=collection_id)
    tags = BottleCap.tags.all().annotate(Count('id')).order_by('-id__count', 'slug')

    context = {
        'slug': slug,
        'collection_id': collection.id,
        'collection_type_name': collection.type.name,
        'collection_owner_username': collection.owner,
        'search_results': BottleCap.objects.filter(tags__slug__exact=slug, collection_id=collection.id),
        'tags': tags
    }

    return render(request, 'collectionsapp/tag_search.html', context)


''''@login_required
def upload_image(request, collection_item_id):
    collection_item = get_object_or_404(BottleCap, pk=collection_item_id)

    if collection_item.collection.owner != request.user:
        messages.warning(request, 'You cannot edit other peoples collections.')
        return redirect('home')

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
                im = Image.open(storage.open(new_image.image.name, 'rb'))

                width, height = im.size

                square_edge_length = 200
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

                # crop
                if new_width > target_width:
                    left = int((new_width - target_width)/2)
                    right = left + target_width
                elif new_height > target_height:
                    top = int((new_height - target_height)/2)
                    bottom = top + target_height

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
                    new_image.image.name.split("images/", 1)[1],
                    InMemoryUploadedFile(
                        pillow_image,
                        None,               # field_name
                        'my_image.jpg',     # file name
                        'image/jpeg',       # content_type
                        pillow_image.tell,  # size
                        None
                    )
                )

            return redirect('bottle_cap', item_id=collection_item_id)
        else:
            print(formset.errors)
    else:
        collection = BottleCap.objects.get(pk=collection_item_id).collection

        context = {
            'collection_item_id': collection_item_id,
            'imageUploadFormSet': collection_item_image_formset(queryset=CollectionItemImage.objects.none())
        }

        return render(request, 'collectionsapp/upload_image.html', context)'''


@login_required
def edit_collection(request, collection_id):
    collection = get_object_or_404(Collection, pk=collection_id)

    if collection.owner != request.user:
        messages.warning(request, "You cannot edit other people's collections.")
        return redirect('home')

    if request.method == "POST":
        form = CollectionEditForm(request.POST, instance=collection)

        if form.is_valid():
            form_data = form.save(commit=False)
            form_data.modified_by = request.user

            form_data.save()

            form.save_m2m()
            return explore_collection(request, collection_id, 'image')
    else:
        form = CollectionEditForm(instance=collection)

    context = {
        'form': form,
        'collection_owner': collection.owner,
        'collection_id': collection_id
    }

    return render(request, 'collectionsapp/edit_collection.html', context)


@login_required
def edit_collection_item(request, collection_item_id):
    collection_item = get_object_or_404(BottleCap, pk=collection_item_id)

    if collection_item.collection.owner != request.user:
        messages.warning(request, 'You cannot edit other people\'s collections.')
        return redirect('home')

    if request.method == "POST":
        form = BottleCapForm(request.POST, request.FILES, instance=collection_item)

        if form.is_valid():
            collection_item = form.save(commit=False)
            collection_item.modified_by = request.user
            collection_item.created_by = collection_item.created_by

            # TODO: if image changes...
            if True:
                new_image = form.cleaned_data['image']

                pillow_image = image_helper.generate_thumbnail(new_image)
                collection_item.image_thumbnail.save(
                    new_image.name,
                    InMemoryUploadedFile(
                        pillow_image,
                        None,               # field_name
                        'my_image.jpg',     # file name
                        'image/jpeg',       # content_type
                        pillow_image.tell,  # size
                        None
                    )
                )

            collection_item.save()

            form.save_m2m()

            messages.success(request, 'Collection item updated.')
            return redirect('bottle_cap', item_id=collection_item.pk)
    else:
        context = {
            'form': BottleCapForm(instance=collection_item),
            'collection_item_id': collection_item_id,
            'collection_owner': collection_item.collection.owner,
            'item_image': collection_item.image
        }
        return render(request, 'collectionsapp/edit_collection_item.html', context)


@login_required
def delete_collection(request, collection_id):
    instance = Collection.objects.get(id=collection_id)
    
    if instance.owner == request.user:
        delete_helper.delete_collection_object(collection_id)
        messages.success(request, 'Collection deleted.')
    else:
        messages.warning(request, 'You must be the owner of this collection to delete.')

    return redirect('my_collections')


@login_required
def delete_collection_item(request, collection_item_id):
    instance = BottleCap.objects.get(id=collection_item_id)
    collection_id = instance.collection_id

    if instance.collection.owner == request.user:
        delete_helper.delete_collection_item_object(collection_item_id)
        messages.success(request, 'Collection item deleted.')
    else:
        messages.warning(request, 'You must be the owner of this collection to delete.')

    return redirect('explore_collection', collection_id=collection_id, view="image")


def search(request):
    criteria = request.GET.get('q')

    # log search
    new_search_action = SearchAction(
        timestamp=datetime.datetime.now(),
        user=None if request.user.is_anonymous else request.user,
        text=criteria
    )
    new_search_action.save()

    context = {
        'criteria': criteria if criteria is not None else ""
    }
    return render(request, 'collectionsapp/search.html', context)


@login_required
def multi_upload(request):
    context = {}
    return render(request, 'collectionsapp/multi_upload.html', context)


@login_required
def post_file(request):
    if request.method == "POST":
        create_collection_item_from_image(request)
    return HttpResponse("Post success")


def create_collection_item_from_image(request):
    uploader = request.user
    collection_id = int(request.POST['collection_id'])
    uploaded_image = request.FILES['file']

    target_collection = Collection.objects.get(id=collection_id)

    current_timestamp = datetime.datetime.now()

    # Create thumbnail
    pillow_image = image_helper.generate_thumbnail(uploaded_image)

    # Create collection item
    bc = BottleCap(
        company="unidentified",
        image=request.FILES['file'],
        image_thumbnail=pillow_image,
        created_by=uploader,
        modified_by=uploader,
        date_acquired=current_timestamp.date(),
        collection=target_collection

    )
    bc.save()

    # TODO: Test this
    bc.image_thumbnail.save(
        uploaded_image.name,
        InMemoryUploadedFile(
            pillow_image,
            None,  # field_name
            'my_image.jpg',  # file name
            'image/jpeg',  # content_type
            pillow_image.tell,  # size
            None
        )
    )


@login_required
def manage_account(request):
    context = {
        'account_delete_form': AccountDeleteForm,
        'target_user': request.user
    }
    return render(request, 'collectionsapp/manage_account.html', context)


@login_required
def delete_account(request, target_user_id):
    if target_user_id == request.user.id:
        delete_helper.delete_user_object(request.user.id)
        messages.success(request, "Account deleted.")
    else:
        messages.warning(request, "Invalid action.")
        
    return redirect('logout')


@staff_member_required
def admin_tools(request):
    return render(request, 'collectionsapp/admin_tools.html')
