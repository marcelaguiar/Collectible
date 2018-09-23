"""Collectible URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from collectionsapp import views


urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('collection_types/', views.collection_types, name='collection_types'),
    path('create_collection/', views.create_collection, name='create_collection'),
    path('create_collection_type/', views.create_collection_type, name='create_collection_type'),
    path('create_item', views.create_item, name='create_item'),
    path('design_fieldset', views.design_fieldset, name='design_fieldset'),
    path('explore_collection/<int:collection_id>/', views.explore_collection, name='explore_collection'),
    path('explore_collection_type/<int:collection_type_id>/', views.explore_collection_type, name='explore_collection_type'),
    path('input_item_details/<int:collection_id>/', views.input_item_details, name='input_item_details'),
    path('item/<int:item_id>/', views.item, name='item'),
    path('logout/', views.logout_view, name='logout'),
    path('my_collections/', views.my_collections, name='my_collections'),
    path('select_collection/', views.select_collection, name='select_collection'),
    path('select_fieldset', views.select_fieldset, name='select_fieldset'),
    path('select_existing_fieldset', views.select_existing_fieldset, name='select_existing_fieldset'),
    path('signup/', views.signup, name='signup'),
    path('site_management/', views.site_management, name='site_management'),
    path('start_collection/', views.start_collection, name='start_collection'),
]
