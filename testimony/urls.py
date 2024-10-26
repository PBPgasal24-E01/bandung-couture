from testimony.views import *
from django.urls import path

app_name = "testimony"

urlpatterns = [
    path('merchant_json/<str:id>/', show_testimony_by_merchant_json, name='show_testimony'),
    path('merchant/<str:id>/', show_testimony_by_merchant, name='show_testimony_by_merchant'),
    path('add_testimony/', create_new_testimony, name='create_new_testimony'),
    path('get_rating/<str:id>/', get_merchant_rating, name='get_rating'), 
    path('delete/<str:id>/', delete_testimony, name='delete_testimony')
]