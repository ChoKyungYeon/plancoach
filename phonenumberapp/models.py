from datetime import timezone

from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

from accountapp.models import CustomUser


class Phonenumber(models.Model):
    phonenumber = models.CharField(max_length=11)
    verification_code = models.CharField(max_length=6)
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='phonenumber', null=True, blank=True)
    is_verified=models.BooleanField(default=False)
    error_count=models.IntegerField(default=0)
