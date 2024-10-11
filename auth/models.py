from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser): 
    VISITOR = 1
    CONTRIBUTOR = 2
    
    ROLE_CHOICES = (
        (VISITOR, 'VISITOR'),
        (CONTRIBUTOR, 'CONTRIBUTOR')
    )
    
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    
     