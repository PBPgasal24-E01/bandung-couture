from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
#class User(AbstractUser):
#  VISITOR = 1
#  CONTRIBUTOR = 1
#  
#
#  ROLE_CHOICES = (
#      (VISITOR, 'Visitor'),
#      (CONTRIBUTOR, 'Contributor'),
#  )
#  role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
#  # You can create Role model separately and add ManyToMany if user has more than one role