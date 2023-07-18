from django.db import models

from accountapp.models import CustomUser


class Refusal(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='refusal')
    content = models.CharField(max_length=15)

