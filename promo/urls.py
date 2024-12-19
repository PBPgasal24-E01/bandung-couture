from django.urls import path
from .views import (
    show_promo,
    create_promo,
    update_promo,
    delete_promo,
    get_promo,
    filter_promos,
    show_json,
    show_json_user,
    create_promo_flutter,
    edit_promo_flutter,
    delete_promo_flutter
)

app_name = 'promo' 

urlpatterns = [
    path('', show_promo, name='show_promo'),  
    path('<uuid:id>/', show_promo, name='show_promo_by_id'),  
    path('create/', create_promo, name='create_promo'),
    path('update/<uuid:id>/', update_promo, name='update_promo'),
    path('get/<uuid:id>/', get_promo, name='get_promo'),
    path('delete/<uuid:id>/', delete_promo, name='delete_promo'),
    path('filter/', filter_promos, name='filter_promos'),
    path('json/', show_json, name='show_json'),
    path('json_own/', show_json_user, name='show_json_user'),
    path('create_promo_flutter/', create_promo_flutter, name='create_promo_flutter'),
    path('edit_promo_flutter/<uuid:id>/', edit_promo_flutter, name='edit_promo_flutter'),
    path('delete_promo_flutter/<uuid:id>/', delete_promo_flutter, name='delete_promo_flutter'),
]