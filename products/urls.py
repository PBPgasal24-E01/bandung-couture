from django.urls import path
from django.shortcuts import redirect
from products.views import show

app_name = 'products'

urlpatterns=[
    path('', lambda request: redirect('products:show'), name='default'),
    path('show', show, name='show'),
]