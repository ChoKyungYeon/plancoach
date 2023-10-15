from django.db import models

from accountapp.models import CustomUser


# Create your models here.
class Review(models.Model):
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='review')
    image = models.ImageField(upload_to='review/', null=True, blank=True)
    content = models.TextField(max_length=300)