from django.db import models
from consult_feedbackapp.models import Consult_feedback
from plancoach.choice import subjectchoice
from plancoach.variables import subjectdictionary, weekdaydictionary


class Feedback_plan(models.Model):
    consult_feedback = models.ForeignKey(Consult_feedback, on_delete=models.CASCADE, related_name='feedback_plan')
    plantime = models.DateField()
    content = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def weekdayimage(self):
        if self.plantime:
            return weekdaydictionary[self.plantime.strftime('%A')]
