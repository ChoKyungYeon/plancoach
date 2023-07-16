from datetime import timedelta, date

from django.db import models, transaction

from accountapp.models import CustomUser
from plancoach.choice import teacherstatechoice, tuitionchoice
from plancoach.sms import Send_SMS
from plancoach.variables import current_date


class Profile(models.Model):
    teacher = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    state = models.CharField(max_length=20, choices=teacherstatechoice, default='disabled')
    tuition = models.IntegerField(choices=tuitionchoice, default=16)
    payment_updated_at = models.DateField(null=True,blank=True)

    def __str__(self):
        return f"{self.teacher.username}({self.teacher.userrealname} 프로필"

    def is_payment_updated_possible(self):
        if not self.payment_updated_at or self.payment_updated_at + timedelta(days=59) < current_date:
            return True
        return (self.payment_updated_at + timedelta(days=60) - current_date).days


    def save(self, *args, **kwargs):
        created = not self.pk
        if created:
            with transaction.atomic():
                content = '선생님 프로필이 생성되었습니다. 프로필을 완성하고 대시보드에서 활성화하세요!'
                user = self.teacher
                Send_SMS(user.username, content, user.can_receive_notification)
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        with transaction.atomic():
            self.teacher.state = 'student'
            self.teacher.save()
            super().delete(*args, **kwargs)
