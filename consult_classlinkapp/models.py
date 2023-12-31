from datetime import datetime
import uuid
from django.db import models
from consultapp.models import Consult
from plancoach.choice import weekdatechoice
from plancoach.variables import weekdaylist



class Consult_classlink(models.Model):
    #uuid
    consult = models.OneToOneField(Consult, on_delete=models.CASCADE, related_name='consult_classlink')
    weekdate = models.CharField(max_length=20, choices=weekdatechoice)
    classtime = models.CharField(max_length=10)
    link = models.TextField(max_length=100, null=True,blank=True)

    def weekdate_left(self):
        today = datetime.now().date().strftime('%A')
        current_index = weekdaylist.index(today)
        target_index = [choice[0] for choice in weekdatechoice].index(self.weekdate)
        if current_index <= target_index:
            days_left = target_index - current_index
        else:
            days_left = 7 - (current_index - target_index)
        return f'{days_left}일뒤' if not days_left == 0 else '금일'
