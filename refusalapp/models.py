from django.db import models

from accountapp.models import CustomUser
from plancoach.choice import refusaltypechoice


class Refusal(models.Model):
    type = models.CharField(max_length=30, choices=refusaltypechoice, default='matching')
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='refusal')
    content = models.CharField(max_length=22, null=True)

