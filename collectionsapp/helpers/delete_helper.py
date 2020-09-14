from collectionsapp.models import BottleCap, Collection, User


def delete_user_object(user_id):
    user = User.objects.get(pk=user_id)
    for collection in Collection.objects.filter(owner_id=user.id):
        delete_collection_object(collection.id)
    
    user.delete()


def delete_collection_object(collection_id):
    collection = Collection.objects.get(pk=collection_id)
    collection_items = BottleCap.objects.filter(collection_id=collection.pk)
    
    for item in collection_items:
        delete_collection_item_object(item.pk)
    
    collection.delete()


def delete_collection_item_object(item_id):
    collection_item = BottleCap.objects.get(pk=item_id)

    if collection_item.image_thumbnail:
        collection_item.image_thumbnail.delete(save=False)
    if collection_item.image:
        collection_item.image.delete(save=False)

    collection_item.delete()
