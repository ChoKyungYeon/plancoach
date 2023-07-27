from django.db import models
from multiselectfield import MultiSelectField
from consultapp.models import Consult
from plancoach.choice import subjectchoice


class Consult_feedback(models.Model):
    consult = models.ForeignKey(Consult, on_delete=models.CASCADE, related_name='consult_feedback')
    subjects = MultiSelectField(max_length=100, choices=subjectchoice)
    content = models.TextField(max_length=1000, null=True)
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

    def plan_done_ratio(self):
        plans = self.feedback_plan.all().order_by('plantime')
        plan_done = sum(plan.is_done for plan in plans)
        ratio = round(plan_done / 7 * 100)
        return [plan_done, ratio] if plan_done != 0 else [0,0]

