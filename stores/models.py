from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=31, unique=True)
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Store(models.Model):
    brand = models.CharField(max_length=31)
    description = models.TextField(null=True)
    categories = models.ManyToManyField(Category)
    address = models.TextField()
    contact_number = models.CharField(max_length=16)
    website = models.URLField()
    social_media = models.CharField(max_length=31)

    def __str__(self):
        return self.brand


