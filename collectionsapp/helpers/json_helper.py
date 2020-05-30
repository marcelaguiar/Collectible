from collectionsapp.models import BeverageType, BottleCap, Collection, CollectionItemImage
from django.http import JsonResponse


def get_all_bottle_caps(request):
    data = BottleCap.objects.all().values('id', 'company', 'brand', 'product', 'variety', 'beverage_type', 'region',
                                          'date_acquired')

    return JsonResponse(list(data), safe=False)


def get_all_bottle_caps_by_collection(request, collection_id):
    data = BottleCap.objects.filter(collection_id=collection_id)\
        .values('id', 'company', 'brand', 'product', 'variety', 'beverage_type', 'region', 'date_acquired')

    return JsonResponse(list(data), safe=False)


def get_all_bottle_caps_with_primary_image(request):
    data = CollectionItemImage.objects.select_related(order_in_collection=1).values()

    data = data.values('id', 'company', 'brand', 'product', 'variety', 'beverage_type', 'date_acquired')

    return JsonResponse(list(data), safe=False)


def get_all_beverage_types(request):
    data = BeverageType.objects.all().values('id', 'name')

    return JsonResponse(list(data), safe=False)


def get_users_collections(request, user_id):
    data = Collection.objects.filter(owner_id=user_id).values('id', 'name')

    return JsonResponse(list(data), safe=False)