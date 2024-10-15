from django.urls import path
from django.shortcuts import redirect
from stores.views import show

app_name = 'stores'

urlpatterns=[
    path('', lambda request: redirect('stores:show'), name='default'),
    path('show', show, name='show'),
]