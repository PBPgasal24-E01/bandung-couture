from django.db import models
from account.models import User
from stores.models import Store

# Create your models here
class Testimony(models.Model):
    testimony = models.TextField()
    rating = models.IntegerField()
    storeId = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    userId = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.testimony