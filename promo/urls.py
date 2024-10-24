from django.urls import path
from .views import show_promo, create_promo, update_promo, delete_promo, rewards_promo_view, redeem_promo, history_promo_view, get_total_redeemed, delete_history
from uuid import UUID

app_name = 'promo'  

urlpatterns = [
    path('', show_promo, name='show_promo'), 
    path('create-promo/', create_promo, name='create_promo'), 
    path('update-promo/<uuid:id>', update_promo, name = 'update_promo'),
    path('delete-promo/<uuid:id>', delete_promo, name = 'delete_promo'),
    path('rewards-promo-view/', rewards_promo_view, name='rewards_promo'),
    path('redeem/<uuid:promo_id>/', redeem_promo, name='redeem_promo'), 
    path('get-total-redeemed/', get_total_redeemed, name='get_total_redeemed'),
    path('history/', history_promo_view, name='history_promo'),
    path('history/delete/<int:history_id>/', delete_history, name='delete_history'),
    
 ] 