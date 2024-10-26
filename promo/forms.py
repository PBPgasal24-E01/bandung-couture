from django.forms import ModelForm
from .models import Promo
from django import forms
from django.utils import timezone


class PromoEntryForm(ModelForm):
    class Meta:
        model = Promo
        fields = ["title", "description", "discount_percentage", "start_date", "end_date", "promo_code", "is_active"]
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if start_date >= end_date:
                raise forms.ValidationError("Tanggal mulai harus sebelum tanggal berakhir.")

            if start_date < timezone.now():
                raise forms.ValidationError("Tanggal mulai tidak valid")

        return cleaned_data
    

    