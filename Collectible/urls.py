from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from collectionsapp import views


urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('add_to_collection/<int:collection_id>/', views.add_to_collection, name='add_to_collection'),
    path('admin/', admin.site.urls),
    path('bottle_cap/<int:item_id>/', views.bottle_cap, name='bottle_cap'),
    path('collection_types/', views.collection_types, name='collection_types'),
    path('create_collection/', views.create_collection, name='create_collection'),
    path('create_collection_type/', views.create_collection_type, name='create_collection_type'),
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
    path('get_all_beverage_types/', views.get_all_beverage_types),
    path('get_all_bottle_caps/', views.get_all_bottle_caps),
    path('get_all_bottle_caps_by_collection/<int:collection_id>/', views.get_all_bottle_caps_by_collection,
         name='get_all_bottle_caps_by_collection'),
    path('get_n_thumbnails/<int:start>/<int:end>', views.get_n_thumbnails, name='get_n_thumbnails'),
    path('get_users_collections/<int:user_id>/', views.get_users_collections),
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
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('search/', views.search, name='search'),
    path('select_collection/', views.select_collection, name='select_collection'),
    path('select_existing_fieldset', views.select_existing_fieldset, name='select_existing_fieldset'),
    path('select_fieldset', views.select_fieldset, name='select_fieldset'),
    path('start_collection/', views.start_collection, name='start_collection'),
    path('tag_search_all_collection_types/<int:collection_id>/<slug:slug>/', views.tag_search_all_collection_types, name='tag_search_all_collection_types'),
    path('tag_search_collection/<int:collection_id>/<slug:slug>/', views.tag_search_collection, name='tag_search_collection'),
    path('tag_search_collection_type/<int:collection_id>/<slug:slug>/', views.tag_search_collection_type, name='tag_search_collection_type'),
    path('multi_upload/', views.multi_upload, name='multi_upload'),
    path('upload_image/<int:collection_item_id>', views.upload_image, name='upload_image'),
    path('manage_account/', views.manage_account, name='manage_account')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
