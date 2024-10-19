from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import uuid
from django.conf import settings

class Promo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    promo_code = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    image = models.ImageField(upload_to='promo_images/', blank=True, null=True)  #

    def __str__(self):
        return self.title

    def is_valid(self):
        return self.is_active and self.start_date <= timezone.now() <= self.end_date
    
class RedeemedPromo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Gunakan AUTH_USER_MODEL
    promo = models.ForeignKey(Promo, on_delete=models.CASCADE)
    redeem_date = models.DateTimeField(auto_now_add=True)

