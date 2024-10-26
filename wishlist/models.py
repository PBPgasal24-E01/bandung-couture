from django.db import models
from account.models import User
from stores.models import Store

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.store.brand} in {self.user.username}'s Wishlist"
