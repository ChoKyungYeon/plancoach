from django.db import models
import uuid
from plancoach.choice import bankchoice
from plancoach.variables import bankdictionary
from profileapp.models import Profile


class Deposit(models.Model):
    #uuid
    bank = models.CharField(max_length=20, choices=bankchoice)
    accountnumber = models.CharField(max_length=30)
    depositor = models.CharField(max_length=20)

    def bankimage(self):
        return bankdictionary[self.bank] if self.bank else None

