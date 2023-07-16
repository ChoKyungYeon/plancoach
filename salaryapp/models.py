from datetime import date

from django.db import models
from django.db.models import Sum

from accountapp.models import CustomUser
from plancoach.choice import bankchoice
from plancoach.variables import bankdictionary


# Create your models here.
class Salary(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='salary')
    salaryday=models.DateField()
    bank = models.CharField(max_length=20, choices=bankchoice,null=True)
    accountnumber = models.CharField(max_length=30,null=True)
    depositor = models.CharField(max_length=10,null=True)
    is_given=models.BooleanField(default=False)
    def bankimage(self):
        return bankdictionary[self.bank] if self.bank else None

    def salary_startdate(self):
        target_date=self.salaryday
        return date(target_date.year + (target_date.month - 2) // 12, (target_date.month - 2) % 12 + 1, 10)

    def payment_amount(self):
        return self.payment.aggregate(total=Sum('amount'))['total'] or 0

    def refund_amount(self):
        return self.refund.aggregate(total=Sum('amount'))['total'] or 0

    def total_amount(self):
        return self.payment_amount()-self.refund_amount()

    def charge_amount(self):
        return int(round(self.total_amount() * 0.25, -2))

    def paid_amount(self):
        return self.total_amount()-self.charge_amount()


