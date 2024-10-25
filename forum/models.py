from django.db import models
import uuid
from account.models import User

# Create your models here.
class Forum(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subforum',
        null=True,
        blank=True
    )
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    details = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self): 
        return self.title