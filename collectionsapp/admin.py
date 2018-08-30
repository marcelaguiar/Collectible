from django.contrib import admin
from .models import CollectionType, BottleCap, Collection

# Register your models here.
admin.site.register(CollectionType)
admin.site.register(BottleCap)
admin.site.register(Collection)
