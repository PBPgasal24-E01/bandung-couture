from django.forms import ModelForm
from .models import Promo
from django import forms
from django.utils import timezone
from django.utils.html import strip_tags

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
    
    
    def clean_title(self):
        title = self.cleaned_data.get("title")
        return strip_tags(title)

    def clean_description(self):
        description = self.cleaned_data.get("description")
        return strip_tags(description)

    def clean_discount_percentage(self):
        discount_percentage = self.cleaned_data.get("discount_percentage")
        if discount_percentage < 1 or discount_percentage > 100:
            raise forms.ValidationError("Discount percentage must be between 1 and 100.")
        return discount_percentage

    def clean_promo_code(self):
        promo_code = self.cleaned_data.get("promo_code")
        return strip_tags(promo_code)

    def clean_start_date(self):
        start_date = self.cleaned_data.get("start_date")
        return start_date

    def clean_end_date(self):
        end_date = self.cleaned_data.get("end_date")
        return end_date

    def clean_is_active(self):
        is_active = self.cleaned_data.get("is_active")
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")

        if is_active and (start_date > timezone.now() or end_date < timezone.now()):
            raise forms.ValidationError("Cannot activate a promo outside its valid date range.")
        return is_active
