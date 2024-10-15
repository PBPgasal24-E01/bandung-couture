from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=31)

class Store(models.Model):
    brand = models.CharField(max_length=31)
    description = models.TextField(null=True)
    category = models.ManyToManyField(Category)
    address = models.TextField()
    contact_number = models.IntegerField()
    website = models.URLField()
    instagram_account = models.CharField(max_length=31)


