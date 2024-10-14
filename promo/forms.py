from django.forms import ModelForm
from .models import Promo

class PromoEntryForm(ModelForm):
    class Meta:
        model = Promo
        fields = ["title", "description", "discount_percentage", "start_date", "end_date", "promo_code", "is_active"]
        