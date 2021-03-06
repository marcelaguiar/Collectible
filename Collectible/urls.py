from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from collectionsapp import views
from collectionsapp.helpers import json_helper


urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('add_to_collection/<int:collection_id>/', views.add_to_collection, name='add_to_collection'),
    path('admin/', admin.site.urls),
    path('admin_tools/', views.admin_tools, name='admin_tools'),
    path('bottle_cap/<int:item_id>/', views.bottle_cap, name='bottle_cap'),
    path('collections/', views.collections, name='collections'),
    path('collection_types/', views.collection_types, name='collection_types'),
    path('create_collection/', views.create_collection, name='create_collection'),
    path('delete_account/<int:target_user_id>/', views.delete_account, name='delete_account'),
    path('delete_collection/<int:collection_id>', views.delete_collection, name='delete_collection'),
    path('delete_collection_item/<int:collection_item_id>', views.delete_collection_item,
         name='delete_collection_item'),
    path('design_fieldset', views.design_fieldset, name='design_fieldset'),
    path('edit_collection/<int:collection_id>/', views.edit_collection, name='edit_collection'),
    path('edit_collection_item/<int:collection_item_id>/', views.edit_collection_item, name='edit_collection_item'),
    path('explore_collection/<int:collection_id>/<str:view>', views.explore_collection, name='explore_collection'),
    path('explore_collection_type/<int:collection_type_id>/', views.explore_collection_type,
         name='explore_collection_type'),
    path('get_all_beverage_types/', json_helper.get_all_beverage_types),
    path('get_all_bottle_caps/', json_helper.get_all_bottle_caps),
    path('get_all_bottle_caps_by_collection/<int:collection_id>/', json_helper.get_all_bottle_caps_by_collection,
         name='get_all_bottle_caps_by_collection'),
    path('get_all_bottle_caps_with_image_by_collection/<int:collection_id>/',
         json_helper.get_all_bottle_caps_with_image_by_collection, name='get_all_bottle_caps_with_image_by_collection'),
    path('get_all_collection_item_ids/', json_helper.get_all_collection_item_ids, name='get_all_collection_item_ids'),
    path('get_all_tags/', json_helper.get_all_tags),
    path('get_by_tag_and_collection/<slug:slug>/<int:collection_id>/', json_helper.get_by_tag_and_collection),
    path('get_by_tag/<slug:slug>/', json_helper.get_by_tag),
    path('get_n_thumbnails/<int:start>/<int:end>/<int:collection_id>', views.get_n_thumbnails, name='get_n_thumbnails'),
    path('get_users_collections/<int:user_id>/', json_helper.get_users_collections),
    path('my_collections/', views.my_collections, name='my_collections'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done2.html'),
        name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm2.html'),
        name='password_reset_confirm'),
    path('password-reset-complete', auth_views.PasswordResetCompleteView.as_view(
         template_name='registration/password_reset_complete2.html'),
         name='password_reset_complete'),
    path('post_file/', views.post_file, name='post_file'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('refresh_thumbnails/<int:collection_item_id>/', views.refresh_thumbnails, name='refresh_thumbnails'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('search/', views.search, name='search'),
    path('select_collection/', views.select_collection, name='select_collection'),
    path('select_existing_fieldset', views.select_existing_fieldset, name='select_existing_fieldset'),
    path('start_collection/', views.start_collection, name='start_collection'),
    path('tag_search/<int:collection_id>/<slug:slug>/', views.tag_search,
         name='tag_search'),
    path('multi_upload/', views.multi_upload, name='multi_upload'),
    path('manage_account/', views.manage_account, name='manage_account')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
