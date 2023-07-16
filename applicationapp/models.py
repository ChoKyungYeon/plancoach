from django.db import models, transaction

from accountapp.models import CustomUser
from plancoach.choice import agechoice, applicationstatechoice, sexchoice
from plancoach.sms import Send_SMS
from plancoach.utils import time_converter_expire



class Application(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='application_student')
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='application_teacher')
    age= models.CharField(max_length=20, choices=agechoice)
    belong = models.CharField(max_length=10)
    want = models.TextField(max_length=500)
    problem = models.TextField(max_length=500)
    strategy = models.TextField(max_length=500)
    state= models.CharField(max_length=20, choices=applicationstatechoice, default='applied')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    def expire_waiting(self):
        return time_converter_expire(self.updated_at, 48) if self.updated_at else None

    def expire_matching(self):
        return time_converter_expire(self.updated_at, 168) if self.updated_at else None

    def expire_applied(self):
        return time_converter_expire(self.created_at, 24)

    def __str__(self):
        return f"{self.student.username}({self.student.userrealname}) 신청서"


    def save(self, *args, **kwargs):
        created = not self.pk
        if created:
            with transaction.atomic():
                teacher = self.teacher
                content = f'{self.student.userrealname} 학생이 수업을 신청했습니다. 신청서를 확인해주세요'
                Send_SMS(teacher.username, content, teacher.can_receive_notification)
        super().save(*args, **kwargs)

