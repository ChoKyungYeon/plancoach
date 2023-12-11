from django.db import models

from accountapp.models import CustomUser
from profileapp.models import Profile


# Create your models here.


class Profile_like(models.Model):
    #uuid
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='profile_like')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile_like')

    class Meta:
        unique_together =('student', 'profile')