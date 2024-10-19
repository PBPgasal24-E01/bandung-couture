from account.views import register, login_user, logout_user
from django.urls import path

app_name = 'account'
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout')
]

