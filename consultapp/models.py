from datetime import timedelta, date, datetime
from django.db import models, transaction

from accountapp.models import CustomUser
from applicationapp.models import Application
from plancoach.choice import consultstatechoice, agechoice
from plancoach.sms import Send_SMS
from plancoach.variables import current_date, current_datetime


class Consult(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='consult', null=True, blank=True)
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='consult_student')
    teacher= models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='consult_teacher')
    state = models.CharField(max_length=20, choices=consultstatechoice, default='new')
    age= models.CharField(max_length=20, choices=agechoice)
    belong = models.CharField(max_length=10)
    tuition = models.IntegerField()
    startdate = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def enddate(self):
        return self.startdate + timedelta(days=28) if self.startdate else None

    def extenddate(self):
        return self.startdate + timedelta(days=29) if self.startdate else None

    def extend_enddate(self):
        return self.startdate + timedelta(days=57) if self.startdate else None

    def refund_amount(self):
        today = current_date
        tuition = self.tuition * 10000
        interval = today - self.startdate
        if interval <= timedelta(days=7):
            return int(round(tuition * 3 / 4, -2))
        elif timedelta(days=7) < interval <= timedelta(days=14):
            return int(round(tuition / 2, -2))
        else:
            return 0

    def refund_entire_amount(self):
        return self.refund_amount()+self.tuition*10000 if self.state=='extended' else self.refund_amount()

    def __str__(self):
        return f"{self.student}( {self.belong} ) 수업 ({self.startdate}~{self.enddate()})"

    def consult_name(self):
        return f"{self.teacher.userrealname}T: {self.student.userrealname} 수업"

    def remaining_day(self):
        now = current_date
        if self.enddate():
            interval = (self.enddate() - now).days
            if interval > 0:
                remaining_day = f'{"연장" if self.state != "unextended" else "종료"} {interval}일 전'
            elif interval == 0:
                remaining_day = '금일 연장' if self.state != 'unextended' else '금일 종료'
            else:
                remaining_day = None
            return remaining_day


    def save(self, *args, **kwargs):
        created = not self.pk
        if created:
            with transaction.atomic():
                application = self.application
                application.state = 'waiting'
                application.updated_at = current_datetime
                application.save()
                content = '신규 수업이 생성되었습니다. 입금을 완료하고 수업을 시작하세요!'
                student = self.student
                Send_SMS(student.username, content, student.can_receive_notification)
        super().save(*args, **kwargs)


