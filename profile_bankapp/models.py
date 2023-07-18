from django.db import models

from plancoach.choice import bankchoice
from plancoach.variables import bankdictionary
from profileapp.models import Profile


class Profile_bank(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='profile_bank')
    bank = models.CharField(max_length=20, choices=bankchoice)
    accountnumber = models.CharField(max_length=30)
    depositor = models.CharField(max_length=6)

    def bankimage(self):
        return bankdictionary[self.bank] if self.bank else None

