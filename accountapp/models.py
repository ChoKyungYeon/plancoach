from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models, transaction

from plancoach.choice import userstatechoice


class CustomUser(AbstractUser):
    username = models.CharField(max_length=11, unique=True)
    userrealname = models.CharField(max_length=10)
    email = models.EmailField(max_length=20, unique=True)
    state = models.CharField(max_length=20, choices=userstatechoice, default='student')
    can_receive_notification =models.BooleanField(default=True)
    int_username=models.IntegerField(null=True)

    def __str__(self):
        return f"{self.state}: {self.username}({self.userrealname})"

    def user_phonenumber(self):
        username=self.username
        return f"{username[:3]}-{username[3:7]}-{username[7:]}"

    def user_consult(self):
        consult=getattr(self, 'consult_student',None)
        return consult if consult and consult.state != 'new' else None