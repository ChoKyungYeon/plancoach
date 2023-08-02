from datetime import timedelta, date, datetime

from django.db import models, transaction

from accountapp.models import CustomUser
from plancoach.choice import teacherstatechoice, tuitionchoice
from plancoach.sms import Send_SMS


class Profile(models.Model):
    teacher = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    state = models.CharField(max_length=20, choices=teacherstatechoice, default='disabled')
    tuition = models.IntegerField(choices=tuitionchoice, default=160000) #deploy check
    payment_updated_at = models.DateField(null=True, blank=True)


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