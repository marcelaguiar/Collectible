from django.contrib import admin
from .models import BottleCap, CollectionType, Collection


# Register your models here.
admin.site.register(CollectionType)
admin.site.register(BottleCap)
admin.site.register(Collection)
