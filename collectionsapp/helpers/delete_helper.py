from collectionsapp.models import BottleCap, CollectionType, Collection, CollectionItem, User,\
    CollectionItemImage, CollectionItemImageThumbnail


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
    images = CollectionItemImage.objects.filter(collection_item_id=collection_item.pk)
    thumbnails = CollectionItemImageThumbnail.objects.filter(collection_item_id=collection_item.pk)
    
    for image in images:
        delete_image_object(image.pk)
    
    for thumbnail in thumbnails:
        delete_thumbnail_object(thumbnail.pk)
    
    collection_item.delete()


def delete_image_object(item_id):
    image = CollectionItemImage.objects.get(pk=item_id)
    image.image.delete(save=False)
    image.delete()


def delete_thumbnail_object(item_id):
    thumbnail = CollectionItemImageThumbnail.objects.get(pk=item_id)
    thumbnail.image.delete(save=False)
    thumbnail.delete()
