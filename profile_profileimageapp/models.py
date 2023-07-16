
from django.db import models

from profileapp.models import Profile



class Profile_profileimage(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='profile_profileimage')
    image = models.ImageField(upload_to='profile_profileimage/')
