from datetime import timedelta, datetime
from django.db import models
from accountapp.models import CustomUser
from plancoach.choice import consultstatechoice, agechoice
from plancoach.utils import time_expire
import uuid

class Consult(models.Model):
    #uuid
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='consult_student')
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='consult_teacher')
    state = models.CharField(max_length=20, choices=consultstatechoice, default='new')
    age = models.CharField(max_length=20, choices=agechoice)
    belong = models.CharField(max_length=8)
    tuition = models.IntegerField()
    startdate = models.DateField(null=True, blank=True)  #컨설팅 시작 첫날
    created_at = models.DateTimeField(auto_now_add=True)
    want = models.TextField(max_length=500)
    problem = models.TextField(max_length=500)
    strategy = models.TextField(max_length=500)
    is_warned=models.BooleanField(default=False)

    def __str__(self):
        return self.consult_name()

    def expire_new(self):
        return time_expire(self.created_at, 48)

    def enddate(self): #컨설팅 일자에 포함
        return self.startdate + timedelta(days=28) if self.startdate else None

    def extenddate(self): #컨설팅 일자 종료 다음날, 연장 첫날
        return self.startdate + timedelta(days=29) if self.startdate else None

    def extend_enddate(self): #컨설팅 연장날 끝나는 날, 이날까지 포함
        return self.startdate + timedelta(days=57) if self.startdate else None

    def is_waiting(self):
        return self.payment.filter(is_paid_ok=False).exists()

    def consult_name(self):
        return f"[{self.teacher.userrealname}T] {self.student.userrealname} 컨설팅"

    def refund_amount(self):
        if self.startdate:
            interval = datetime.now().date() - self.startdate
            tuition = self.tuition
            refund_rates = [(timedelta(days=7), 3 / 4), (timedelta(days=14), 1 / 2)]
            for days, rate in refund_rates:
                if interval < days:
                    return int(round(tuition * rate, -2))
        return 0

    def refund_entire_amount(self):
        return self.refund_amount() + self.tuition if self.state == 'extended' else self.refund_amount()

    def can_refund(self):
        return True if self.refund_entire_amount() != 0 and self.is_waiting() == False else False

    def extend_warning(self):
        if self.enddate():
            interval = (self.enddate() - datetime.now().date()).days
            if self.state == 'unextended':
                if interval <= 7:
                    remaining_day = f'{interval}일 후'
                elif interval == 0:
                    remaining_day = '금일'
                else:
                    remaining_day = None
            else:
                remaining_day = None
            return remaining_day

    def remaining_day(self):
        if self.enddate():
            interval = (self.enddate() - datetime.now().date()).days
            if interval > 0:
                remaining_day = f'{"연장" if self.state != "unextended" else "종료"} {interval}일 전'
            elif interval == 0:
                remaining_day = '금일 연장' if self.state != 'unextended' else '금일 종료'
            else:
                remaining_day = None
            return remaining_day

    def has_new_qna(self):
        return self.consult_qna.filter(is_answered=False).exists()


