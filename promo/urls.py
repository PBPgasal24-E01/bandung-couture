from django.urls import path
from .views import (
    show_promo,
    create_promo,
    update_promo,
    delete_promo,
    get_promo,
    filter_promos
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
]