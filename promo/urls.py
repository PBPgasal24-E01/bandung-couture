from django.urls import path
from . import views

app_name = 'promo'  

urlpatterns = [
    path('', views.show_promo, name='show_promo'),  
    path('create-promo/', views.create_promo, name='create_promo'), 
    path('update-promo/<uuid:id>', views.update_promo, name = 'update_promo'),
    path('delete-promo/<uuid:id>', views.delete_promo, name = 'delete_promo')
 ] 