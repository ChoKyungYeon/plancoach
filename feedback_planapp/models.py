from datetime import timedelta, datetime

from django.db import models
from consult_feedbackapp.models import Consult_feedback


class Feedback_plan(models.Model):
    consult_feedback = models.ForeignKey(Consult_feedback, on_delete=models.CASCADE, related_name='feedback_plan')
    plantime = models.DateField()
    content = models.TextField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    is_done = models.BooleanField(default=False)

    def can_check_plan(self):
        return datetime.now().date() == self.plantime or datetime.now().date() == self.plantime +timedelta(days=1)
