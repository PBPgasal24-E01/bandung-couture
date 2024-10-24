from django.contrib import admin
from .models import Promo, RedeemedPromo, HistoryPromo

# Mendaftar model Promo
admin.site.register(Promo)

# Mendaftar model RedeemedPromo
admin.site.register(RedeemedPromo)

# Mendaftar model HistoryPromo
admin.site.register(HistoryPromo)
