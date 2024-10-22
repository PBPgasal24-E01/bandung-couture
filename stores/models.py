from django.db import models
from account.models import User

class Category(models.Model):
    name = models.CharField(max_length=31, unique=True)
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Store(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    brand = models.CharField(max_length=31)
    description = models.TextField(null=True)
    categories = models.ManyToManyField(Category)
    address = models.TextField()
    contact_number = models.CharField(max_length=16)
    website = models.URLField()
    social_media = models.CharField(max_length=31)

    def __str__(self):
        return self.brand


