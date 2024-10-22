from django.forms import ModelForm
from stores.models import Store

class StoreForm(ModelForm):
    class Meta:
        model = Store
        fields = ['brand', 'description', 'categories', 'address', 'contact_number', 'website', 'social_media']