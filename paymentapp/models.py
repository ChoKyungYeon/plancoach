import logging
from datetime import timedelta
from uuid import uuid4

from django.core.validators import MinValueValidator
from django.db import models, transaction
from django.http import Http404
from iamport import Iamport

from accountapp.models import CustomUser
from consultapp.models import Consult
from salaryapp.models import Salary
from salaryapp.utils import salaryday_calculator

try:#deploy check
    from plancoach.settings.local import PORTONE_API_KEY, PORTONE_API_SECRET
except:
    from plancoach.settings.deploy import PORTONE_API_KEY, PORTONE_API_SECRET
from plancoach.sms import Send_SMS

# Create your models here.


logger = logging.getLogger('portone')

class Payment(models.Model):
    class StatusChoice(models.TextChoices):
        READY = 'ready', '미결제'
        PAID = 'paid', '결제완료'
        CANCELLED = 'cancelled', '결제취소'
        FAILED = 'failed', '결제실패'
    status = models.CharField(
        max_length=9,
        default=StatusChoice.READY,
        choices=StatusChoice.choices,
        db_index=True,
    )
    uid = models.UUIDField(default=uuid4, editable=False)
    classname = models.CharField(max_length=100)
    consult = models.ForeignKey(Consult, on_delete=models.SET_NULL,null=True, related_name='payment')
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE,null=True, related_name='payment')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid_ok = models.BooleanField(default=False)
    is_initial_payment = models.BooleanField(default=False)
    amount = models.PositiveIntegerField()



    @property
    def merchant_uid(self) -> str:
        return self.uid.hex

    def portone_check(self, commit=True):
        api= Iamport(
            imp_key=PORTONE_API_KEY, #deploy 바꿔주기
            imp_secret=PORTONE_API_SECRET  #deploy 바꿔주기
        )
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
            target_bank = teacher.profile.profile_bank
            with transaction.atomic():
                if consult.state == 'new':
                    #consult
                    consult.state= 'unextended'
                    consult.startdate = self.created_at.date()
                    consult.save()
                    #application
                    consult.application.state='ongoing'
                    consult.application.save()
                    #sms
                    content = f'({self.classname}) 신규 입금이 완료되었습니다. 수업을 시작해주세요!'
                    Send_SMS(teacher.username, content, teacher.can_receive_notification)
                    salaryday = salaryday_calculator(self.created_at.date() + timedelta(days=28))
                else:
                    self.is_initial_payment = True
                    # consult
                    consult.state= 'extended'
                    consult.save()
                    # sms
                    content = f'({self.classname}) 수업 연장이 완료되었습니다!'
                    Send_SMS(teacher.username, content, teacher.can_receive_notification)
                    salaryday = salaryday_calculator(self.created_at.date() + timedelta(days=57))
                # create salary
                target_salary = teacher.salary.filter(salaryday=salaryday).first()
                if target_salary:
                    self.salary=target_salary
                else:
                    Salary.objects.create(teacher=teacher,salaryday=salaryday)
                    self.salary = teacher.salary.get(salaryday=salaryday)

        if commit:
            self.save()

