from datetime import timedelta, datetime
from django.db import models, transaction
from accountapp.models import CustomUser
from plancoach.choice import agechoice, applicationstatechoice
from plancoach.utils import time_expire

class Application(models.Model):
    #uuid
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE,related_name='application_student')
    teacher = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='application_teacher')
    age = models.CharField(max_length=20, choices=agechoice)
    belong = models.CharField(max_length=8)
    want = models.TextField(max_length=500)
    problem = models.TextField(max_length=500)
    strategy = models.TextField(max_length=500)
    state = models.CharField(max_length=20,choices=applicationstatechoice,default='applied')
    updated_at = models.DateTimeField()


    def expire_matching(self):
        return time_expire(self.updated_at, 168)

    def expire_applied(self):
        return time_expire(self.updated_at, 24)

