import os

from collectionsapp.models import BeverageType, BottleCap, Collection
from django.db.models import Count, F
from django.http import JsonResponse
from django.core.files.storage import get_storage_class


def get_all_bottle_caps(request):
    data = BottleCap.objects.all().values('id', 'company', 'brand', 'product', 'variety', 'beverage_type', 'region',
                                          'date_acquired')

    return JsonResponse(list(data), safe=False)


def get_all_bottle_caps_by_collection(request, collection_id):
    data = BottleCap.objects.filter(collection_id=collection_id)\
        .values('id', 'company', 'brand', 'product', 'variety', 'beverage_type', 'region', 'date_acquired')

    return JsonResponse(list(data), safe=False)


'''def get_all_bottle_caps_with_primary_image(request):
    data = CollectionItemImage.objects.select_related(order_in_collection=1).values()

    data = data.values('id', 'company', 'brand', 'product', 'variety', 'beverage_type', 'date_acquired')

    return JsonResponse(list(data), safe=False)'''


def get_all_beverage_types(request):
    data = BeverageType.objects.all().values('id', 'name')

    return JsonResponse(list(data), safe=False)


def get_users_collections(request, user_id):
    data = Collection.objects.filter(owner_id=user_id).values('id', 'name')

    return JsonResponse(list(data), safe=False)


def get_all_tags(request):
    tags = BottleCap.tags.all().annotate(count=Count('id')).values('name', 'slug', 'count').order_by('-count', 'slug')

    return JsonResponse(list(tags), safe=False)


def get_by_tag_and_collection(request, slug, collection_id):
    items = BottleCap.objects\
               .filter(tags__slug__exact=slug, collection_id=collection_id)\
               .values('id', relative_url=F('image_thumbnail'))

    result_list = add_full_urls(items)

    return JsonResponse(result_list, safe=False)


def get_by_tag(request, slug):
    items = BottleCap.objects.filter(tags__slug__exact=slug).values('id', relative_url=F('image_thumbnail'))

    result_list = add_full_urls(items)

    return JsonResponse(result_list, safe=False)


def add_full_urls(items):
    # instance of the current storage class
    media_storage = get_storage_class()()

    # Construct and add the full url into the dictionary items
    results = [
        {**item, "full_url": media_storage.url(item["relative_url"])}
        for item in items
    ]

    return results
