from datetime import timedelta, date, datetime

from django.db import models, transaction
import uuid
from accountapp.models import CustomUser
from plancoach.choice import tuitionchoice
from plancoach.sms import Send_SMS


class Profile(models.Model):
    #uuid
    teacher = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    is_activated = models.BooleanField(default=False)
    tuition = models.IntegerField(choices=tuitionchoice, default=160000) #deploy check
    payment_updated_at = models.DateField(null=True, blank=True)
    is_highlighted = models.BooleanField(default=False)

    def is_payment_updated_possible(self):
        if not self.payment_updated_at or self.payment_updated_at + timedelta(days=59) < datetime.now().date():
            return True
        return (self.payment_updated_at + timedelta(days=60) - datetime.now().date()).days

    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.teacher.state = 'student'
            self.teacher.save()
            super().delete(*args, **kwargs)

    def tuition_million(self):
        return str(self.tuition)[:2]