from django.urls import path
from django.shortcuts import redirect
from stores.views import *

app_name = 'stores'

urlpatterns=[
    path('', lambda request: redirect('stores:show'), name='default'),
    path('show', show, name='show'),
    path('show-own', show_own, name='show-own'),
    path('add', add, name='add'),
    path('edit/<int:pk>', edit, name='edit'),
    path('delete/<int:pk>', delete, name='delete'),
    path('deliver-all-stores-content-component', deliver_all_stores_content_component, name='deliver-all-stores-content-component'),
    path('deliver-own-stores-content-component', deliver_own_stores_content_component, name='deliver-own-stores-content-component'),
    path('deliver-store-form', deliver_store_form, name='deliver-store-form'),
    path('deliver-store-form/<int:pk>', deliver_store_form, name='deliver-store-form'),
    path('show-rest-all', show_rest_all, name='show-rest-all'),
    path('show-rest-own', show_rest_own, name='show-rest-own'),
    path('add-mobile', add_mobile, name='add-mobile'),
    path('edit-mobile', edit_mobile, name='edit-mobile'),
    path('delete-mobile', delete_mobile, name='delete-mobile'),
    path('get-categories-mapping', get_categories_mapping, name='get-categories-mapping'),
    path('get-store/<int:store_id>/', get_store_by_id, name='get-store'),
]
