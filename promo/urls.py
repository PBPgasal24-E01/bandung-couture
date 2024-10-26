# from django.urls import path
# from .views import show_promo, create_promo, update_promo, delete_promo, rewards_promo_view, redeem_promo, history_promo_view, get_total_redeemed, delete_history, show_json

# app_name = 'promo'  

# urlpatterns = [
#     path('', show_promo, name='show_promo'), 
#     path('create-promo/', create_promo, name='create_promo'), 
#     path('update-promo/<uuid:id>', update_promo, name = 'update_promo'),
#     path('delete-promo/<uuid:id>', delete_promo, name = 'delete_promo'),
#     path('rewards-promo-view/', rewards_promo_view, name='rewards_promo'),
#     path('redeem/<uuid:promo_id>/', redeem_promo, name='redeem_promo'), 
#     path('get-total-redeemed/', get_total_redeemed, name='get_total_redeemed'),
#     path('history/', history_promo_view, name='history_promo'),
#     path('history/delete/<int:history_id>/', delete_history, name='delete_history'),
#     path('show_json/', show_json, name='show_json'),
    
#  ] 


# promo/urls.py

# promo/urls.py
from django.urls import path
from .views import (
    show_promo,
    create_promo,
    update_promo,
    delete_promo,
    get_promo,
)

app_name = 'promo'  # Define the app_name here

urlpatterns = [
    path('', show_promo, name='show_promo'),  
    path('<uuid:id>/', show_promo, name='show_promo_by_id'),  
    path('create/', create_promo, name='create_promo'),
    path('update/<uuid:id>/', update_promo, name='update_promo'),
    path('get/<uuid:id>/', get_promo, name='get_promo'),
    path('delete/<uuid:id>/', delete_promo, name='delete_promo'),
]