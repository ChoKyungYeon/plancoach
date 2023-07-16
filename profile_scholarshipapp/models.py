from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from plancoach.choice import schoolyearchoice, schoolchoice
from profileapp.models import Profile





class Profile_scholarship(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='profile_scholarship')
    accepttype = models.CharField(max_length=15)
    studentid = models.IntegerField(choices=schoolyearchoice)  #validator form 걸기
    content = models.TextField(max_length=500)
    schoolverificationimage = models.ImageField(upload_to='profile_scholarship/')
    school = models.CharField(max_length=20, choices=schoolchoice)
    major = models.CharField(max_length=15)

    def scholarship_name(self):
        return f"{self.school} {self.major} {self.studentid}"
