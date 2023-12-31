from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid
from plancoach.choice import schoolyearchoice
from profileapp.models import Profile


# Create your models here.
class Profile_sat(models.Model):
    #uuid
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_sat')
    satverificationimage = models.ImageField(upload_to='profile_sat/')
    satyear =models.IntegerField(choices=schoolyearchoice) #validator form 걸기
    score = models.TextField(max_length=300)