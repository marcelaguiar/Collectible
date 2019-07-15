from django.contrib import admin
from .models import BeverageType, BottleCap, CollectionType, Collection, CollectionItemImage,\
    CollectionItemImageThumbnail, MethodAcquired


# Register your models here.
admin.site.register(CollectionType)
admin.site.register(BeverageType)
admin.site.register(BottleCap)
admin.site.register(Collection)
admin.site.register(CollectionItemImage)
admin.site.register(CollectionItemImageThumbnail)
admin.site.register(MethodAcquired)
