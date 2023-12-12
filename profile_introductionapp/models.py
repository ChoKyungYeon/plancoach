
from django.db import models
import uuid
from profileapp.models import Profile


class Profile_introduction(models.Model):
    #uuid
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='profile_introduction')
    content =models.TextField(max_length=80)
