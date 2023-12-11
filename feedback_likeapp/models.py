from django.db import models
from accountapp.models import CustomUser
from consult_feedbackapp.models import Consult_feedback


class Feedback_like(models.Model):
    #uuid
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='feedback_like')
    consult_feedback = models.ForeignKey(Consult_feedback, on_delete=models.CASCADE, related_name='feedback_like')

    class Meta:
        unique_together = ('student', 'consult_feedback')
