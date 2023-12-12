from django.db import models
import uuid
from accountapp.models import CustomUser
from plancoach.choice import refusaltypechoice


class Refusal(models.Model):
    #uuid
    type = models.CharField(max_length=30, choices=refusaltypechoice, default='matching')
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='refusal')
    content = models.CharField(max_length=21, null=True)

