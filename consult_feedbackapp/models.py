from django.db import models
from multiselectfield import MultiSelectField
from consultapp.models import Consult
from plancoach.choice import subjectchoice


class Consult_feedback(models.Model):
    consult = models.ForeignKey(Consult, on_delete=models.CASCADE, related_name='consult_feedback')
    subjects = MultiSelectField(max_length=100, choices=subjectchoice)
    content = models.TextField(max_length=1000, default='학생 종합 분석 작성')
    classtime = models.DateField()

    class Meta:
        unique_together = (('consult', 'classtime'),)

    def subjects_list(self):
        text = ''
        for subject in self.subjects:
            if len(text + subject) > 25:
                return text.rstrip(', ') + '...'
            text += subject + ', '
        return text.rstrip(', ')

    def plan_duration(self):
        plans = self.feedback_plan.all().order_by('plantime')
        startdate = plans.first().plantime
        lastdate = plans.last().plantime
        return [startdate, lastdate]
