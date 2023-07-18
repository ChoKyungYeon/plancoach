import logging
from datetime import timedelta
from uuid import uuid4
from django.db import models, transaction
from django.http import Http404
from iamport import Iamport
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
    class StatusChoice(models.TextChoices):
        READY = 'ready', '미결제'
        PAID = 'paid', '결제완료'
        CANCELLED = 'cancelled', '결제취소'
        FAILED = 'failed', '결제실패'
    status = models.CharField(max_length=20, default=StatusChoice.READY, choices=StatusChoice.choices, db_index=True)
    uid = models.UUIDField(default=uuid4, editable=False)
    classname = models.CharField(max_length=100)
    consult = models.ForeignKey(Consult, on_delete=models.SET_NULL, null=True, related_name='payment')
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE, null=True, related_name='payment')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid_ok = models.BooleanField(default=False)
    is_initial_payment = models.BooleanField(default=False)
    amount = models.PositiveIntegerField()


    @property
    def merchant_uid(self) -> str:
        return self.uid.hex

    def portone_check(self, commit=True):
        api= Iamport(imp_key=PORTONE_API_KEY, imp_secret=PORTONE_API_SECRET )
        try:
            meta = api.find(merchant_uid=self.merchant_uid)
        except (Iamport.ResponseError, Iamport.HttpError) as e:
            logger.error(str(e), exc_info=e)
            raise Http404(str(e))
        self.status = meta['status']
        self.is_paid_ok= meta['status'] == 'paid' and meta['amount'] == self.amount

        if self.is_paid_ok == True:
            consult = self.consult
            teacher = consult.teacher
            with transaction.atomic():
                if consult.state == 'new':
                    self.is_initial_payment = True
                    self.new_payment_process(consult,teacher)
                else:
                    self.extend_payment_process(consult,teacher)
        if commit:
            self.save()

    def new_payment_process(self, consult, teacher):
        consult.state = 'unextended'
        consult.startdate = self.created_at.date()
        consult.save()

        salaryday = salaryday_calculator(self.created_at.date() + timedelta(days=28))
        self.add_salary(teacher, salaryday)
        content = f'({self.classname}) 신규 입금이 완료되었습니다. 수업을 시작해주세요!'
        Send_SMS(teacher.username, content, teacher.can_receive_notification)

    def extend_payment_process(self, consult, teacher):
        consult.state = 'extended'
        consult.save()

        salaryday = salaryday_calculator(self.created_at.date() + timedelta(days=57))
        self.add_salary(teacher, salaryday)

        content = f'({self.classname}) 수업 연장이 완료되었습니다!'
        Send_SMS(teacher.username, content, teacher.can_receive_notification)


    def add_salary(self, teacher, salaryday):
        try:
            self.salary = teacher.salary.get(salaryday=salaryday)
        except:
            Salary.objects.create(teacher=teacher, salaryday=salaryday)
            self.salary = teacher.salary.get(salaryday=salaryday)