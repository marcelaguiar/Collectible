from django.contrib import admin
from .models import BeverageType, BottleCap, CollectionType, Collection, MethodAcquired, SearchAction

# Register your models here.
admin.site.register(CollectionType)
admin.site.register(BeverageType)
admin.site.register(BottleCap)
admin.site.register(Collection)
admin.site.register(MethodAcquired)
admin.site.register(SearchAction)
