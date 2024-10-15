from django.db import models
import uuid

class Category(models.Model):
    name = models.CharField(max_length=31)
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Store(models.Model):
    brand = models.CharField(max_length=31)
    description = models.TextField(null=True)
    category = models.ManyToManyField(Category)
    address = models.TextField()
    contact_number = models.IntegerField()
    website = models.URLField()
    instagram_account = models.CharField(max_length=31)

    def __str__(self):
        return self.brand


