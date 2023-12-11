from datetime import date

from django.db import models

from plancoach.choice import subjectchoice, durationchoice, yearchoice
from profileapp.models import Profile





class Profile_career(models.Model):
    #uuid
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_career')
    year = models.IntegerField(choices=yearchoice)
    duration = models.CharField(max_length=20, choices=durationchoice)
    content = models.CharField(max_length=50)
    type = models.CharField(max_length=15)
    subject = models.CharField(max_length=20, choices=subjectchoice)
