
from django.db import models
import uuid
from profileapp.models import Profile



class Profile_profileimage(models.Model):
    #uuid
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='profile_profileimage')
    image = models.ImageField(upload_to='profile_profileimage/')
