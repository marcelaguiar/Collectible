from django.contrib import admin
from .models import BeverageType, BottleCap, CollectionType, Collection, SearchAction

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class MyUserAdmin(UserAdmin):
    ordering = ('-date_joined',)
    list_display = ('username', 'email', 'date_joined', 'is_staff')


# finally replace the default UserAdmin with yours
admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

# Register your models here.
admin.site.register(CollectionType)
admin.site.register(BeverageType)
admin.site.register(BottleCap)
admin.site.register(Collection)
admin.site.register(SearchAction)
