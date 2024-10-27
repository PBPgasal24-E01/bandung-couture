from django.urls import path
from account.views import register, login_user, logout_user

app_name = 'account'

urlpatterns = [
    path('register/', register, name='register'),  # URL untuk registrasi
    path('login/', login_user, name='login'),  # URL untuk login
    path('logout/', logout_user, name='logout'),  # URL untuk logout
]
