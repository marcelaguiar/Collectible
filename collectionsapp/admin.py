from django.contrib import admin
from .models import BottleCap, CollectionType, Collection, CollectionItem, CollectionFieldset, CollectionItemImage
import eav


# Register your models here.
admin.site.register(CollectionType)
admin.site.register(BottleCap)
admin.site.register(Collection)
admin.site.register(CollectionItemImage)
admin.site.register(CollectionFieldset)
eav.register(CollectionItem)

