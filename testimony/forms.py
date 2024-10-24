from django import forms
from django.forms import ModelForm
from testimony.models import Testimony

class TestimonyForm(ModelForm):
    class Meta:
        model = Testimony
        fields = ['testimony', 'rating']
