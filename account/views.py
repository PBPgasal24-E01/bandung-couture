from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib import messages
from django.core import serializers
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import reverse
import datetime

from account.forms import RegistrationForm
 
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  
            # load the profile instance created by the signal
            user.save()

            return redirect('account:login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
  
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                response = HttpResponseRedirect(reverse("main:home"))
                response.set_cookie('last_login', str(datetime.datetime.now()))
                return response

            else :
                print("User is None")

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('account:login'))
    response.delete_cookie('last_login')
    return response