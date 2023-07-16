from django.db import models

from accountapp.models import CustomUser
from plancoach.choice import schoolyearchoice, accepttypechoice, bankchoice, consulttypechoice, schoolchoice
from plancoach.variables import bankdictionary
from multiselectfield import MultiSelectField



# Create your models here.
class Teacherapply(models.Model):
    customuser = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacherapply')
    accepttype = models.CharField(max_length=20, choices=accepttypechoice,null=True)
    studentid = models.IntegerField(choices=schoolyearchoice,null=True)  #validator form 걸기
    schoolimage = models.ImageField(upload_to='teacherapply/')
    userimage = models.ImageField(upload_to='teacherapply/',null=True)
    school = models.CharField(max_length=20, choices=schoolchoice,null=True)
    major = models.CharField(max_length=15,null=True)
    bank = models.CharField(max_length=20, choices=bankchoice,null=True)
    accountnumber = models.CharField(max_length=30, null=True)
    depositor = models.CharField(max_length=10,null=True)
    consulttype = MultiSelectField(max_length=20, choices=consulttypechoice,null=True)

    def bankimage(self):
        return bankdictionary[self.bank] if self.bank else None

    def scholarship_name(self):
        return f"{self.school} {self.major} {self.studentid}"

    def apply_done(self):
        return True if self.studentid else False
