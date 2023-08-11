import logging
from datetime import timedelta
from uuid import uuid4
from django.db import models, transaction
from django.http import Http404
from iamport import Iamport

from accountapp.models import CustomUser
from consultapp.models import Consult
from plancoach.utils import salaryday_calculator
from salaryapp.models import Salary

try:
    from plancoach.settings.local import PORTONE_API_KEY, PORTONE_API_SECRET
except:
    from plancoach.settings.deploy import PORTONE_API_KEY, PORTONE_API_SECRET
from plancoach.sms import Send_SMS


logger = logging.getLogger('portone')

class Payment(models.Model):
    classname = models.CharField(max_length=100)
    consult = models.ForeignKey(Consult, on_delete=models.SET_NULL, null=True, related_name='payment')
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE, null=True, related_name='payment')
    student = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='student')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid_ok = models.BooleanField(default=False)
    is_initial_payment = models.BooleanField(default=False)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"[{self.classname}] {self.amount}원 {self.created_at.strftime('%Y-%m-%d %H:%M')} "

    def update(self):
        with transaction.atomic():
            consult = self.consult
            teacher = consult.teacher
            if consult.state == 'new':
                self.is_initial_payment = True
                self.new_payment_process(consult,teacher)
            else:
                self.extend_payment_process(consult,teacher)
            self.is_paid_ok = True
            self.save()

    def new_payment_process(self, consult, teacher):
        consult.state = 'unextended'
        consult.startdate = self.created_at.date()
        consult.save()

        salaryday = salaryday_calculator(self.created_at.date() + timedelta(days=28))
        self.add_salary(teacher, salaryday)
        content = f'{self.consult.student.userrealname} 학생의 신규 입금이 완료되었습니다. 컨설팅을 시작해 주세요!'
        Send_SMS(teacher.username, content, teacher.can_receive_notification)

    def extend_payment_process(self, consult, teacher):
        consult.state = 'extended'
        consult.save()

        salaryday = salaryday_calculator(self.created_at.date() + timedelta(days=57))
        self.add_salary(teacher, salaryday)

        content = f'{self.consult.student.userrealname} 학생의 컨설팅 연장이 완료되었습니다!'
        Send_SMS(teacher.username, content, teacher.can_receive_notification)


    def add_salary(self, teacher, salaryday):
        try:
            self.salary = teacher.salary.get(salaryday=salaryday)
        except:
            Salary.objects.create(teacher=teacher, salaryday=salaryday)
            self.salary = teacher.salary.get(salaryday=salaryday)
