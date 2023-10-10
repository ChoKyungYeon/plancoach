from django.db import models
from accountapp.models import CustomUser
from plancoach.choice import bankchoice
from plancoach.variables import bankdictionary
from salaryapp.models import Salary


class Refund(models.Model):
    classname = models.CharField(max_length=100)
    salary = models.ForeignKey(Salary, on_delete=models.SET_NULL, null=True, related_name='refund')
    student = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='refund')
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.PositiveIntegerField()
    is_given = models.BooleanField(default=False)
    bank = models.CharField(max_length=20, choices=bankchoice)
    accountnumber = models.CharField(max_length=30)
    depositor = models.CharField(max_length=6)
    given_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"[{self.classname}] {self.amount}원 {self.created_at.strftime('%Y-%m-%d %H:%M')} "

    def bankimage(self):
        return bankdictionary[self.bank] if self.bank else None

