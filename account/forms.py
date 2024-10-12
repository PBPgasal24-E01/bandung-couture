from django.contrib.auth.forms import UserCreationForm
from account.models import User
from django import forms

ROLE_CHOICES = User.ROLE_CHOICES

class RegistrationForm(UserCreationForm):
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'role')