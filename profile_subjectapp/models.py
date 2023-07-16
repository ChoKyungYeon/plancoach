
from django.db import models

from plancoach.choice import subjectchoice
from profileapp.models import Profile



# Create your models here.
class Profile_subject(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_subject')
    subjectdetail = models.CharField(max_length=15)
    subjectclassification = models.CharField(max_length=20, choices=subjectchoice)
    content = models.TextField(max_length=500)
