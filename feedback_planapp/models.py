from django.db import models
from consult_feedbackapp.models import Consult_feedback


class Feedback_plan(models.Model):
    consult_feedback = models.ForeignKey(Consult_feedback, on_delete=models.CASCADE, related_name='feedback_plan')
    plantime = models.DateField()
    content = models.TextField(max_length=1000, null=True, blank=True, default='학습 플랜 작성')
    created_at = models.DateTimeField(auto_now=True)

