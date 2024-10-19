from django.urls import path
from . import views
from uuid import UUID

app_name = 'promo'  

urlpatterns = [
    path('', views.show_promo, name='show_promo'),  
    path('create-promo/', views.create_promo, name='create_promo'), 
    path('update-promo/<uuid:id>', views.update_promo, name = 'update_promo'),
    path('delete-promo/<uuid:id>', views.delete_promo, name = 'delete_promo'),
    path('rewards-promo-view/', views.rewards_promo_view, name='rewards_promo'),
    path('redeem/<uuid:promo_id>/', views.redeem_promo, name='redeem_promo'), 
    path('history/', views.history_promo_view, name='history_promo'),
    path('get-total-redeemed/', views.get_total_redeemed, name='get_total_redeemed'),
 ] 