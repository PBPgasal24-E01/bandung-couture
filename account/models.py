from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class User(AbstractUser):
  VISITOR = 1
  CONTRIBUTOR = 2
  ROLE_CHOICES = (
      (VISITOR, 'Visitor'),
      (CONTRIBUTOR, 'Contributor'),
  )
  role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
  
  def __str__(self):
    return self.username