from django.contrib import admin
from .models import BottleCap, CollectionType, Collection, CollectionItem
import eav


# Register your models here.
admin.site.register(CollectionType)
admin.site.register(BottleCap)
admin.site.register(Collection)
eav.register(CollectionItem)

