from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from plancoach.choice import highschooltypechoice
from profileapp.models import Profile



# Create your models here.
class Profile_gpa(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='profile_gpa')
    gpaverificationimage = models.ImageField(upload_to='profile_gpa/', blank=True, null=True)
    highschool = models.CharField(max_length=10)
    schooltype= models.CharField(max_length=20, choices=highschooltypechoice)
    score = models.TextField(max_length=300)