from django.urls import path
from django.shortcuts import redirect
from main.views import *

app_name = 'main'

urlpatterns = [
    path('', lambda request: redirect('main:home'), name='default'),
    path('home', home, name='home'),
]