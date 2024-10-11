from auth.views import register
from django.urls import path

app_name = 'auth'

urlpatterns = [
    path('register/', register, name="register"),
]