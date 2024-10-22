from django.urls import path
from django.shortcuts import redirect
from stores.views import show, show_own, add

app_name = 'stores'

urlpatterns=[
    path('', lambda request: redirect('stores:show'), name='default'),
    path('show', show, name='show'),
    path('show-own', show_own, name='show-own'),
    path('add', add, name='add'),
]