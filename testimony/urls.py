from testimony.views import *
from django.urls import path

app_name = "testimony"

urlpatterns = [
    path('merchant_json/<str:id>/', show_testimony_by_merchant_json, name='show_testimony'),
    path('merchant/<str:id>/', show_testimony_by_merchant, name='show_testimony_by_merchant'),
    path('add_testimony/', create_new_testimony, name='create_new_testimony'),

    path('add_testimony_flutter/', add_testimony_flutter, name='create_new_testimony_flutter'),
    path('edit_testimony_flutter/', edit_testimony_flutter, name='edit_testimony_flutter'),
    path('delete_testimony_flutter/<str:id>/', delete_testimony_flutter, name='delete_testimony_flutter'),

    path('exist_testimony_by_store/<str:id>/', exist_testimony_in_store, name='exist_testimony'),

    path('get_all_merchant/<str:id>/', get_all_testimony_by_id, name='get_all_testimony_by_id'),
    path('get_all_merchant/', get_all_store, name='get_all_merchant'),


    path('get_rating/<str:id>/', get_merchant_rating, name='get_rating'), 
    path('get_number_of_rating/<str:id>/', get_number_of_rating, name='get_number_of_rating'), 

    path('delete/<str:id>/', delete_testimony, name='delete_testimony')
]