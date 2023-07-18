from django.db import models
from consult_feedbackapp.models import Consult_feedback
from plancoach.choice import subjectchoice
from plancoach.variables import subjectdictionary


class Feedback_coach(models.Model):
    consult_feedback = models.ForeignKey(Consult_feedback, on_delete=models.CASCADE, related_name='feedback_coach')
    subject = models.CharField(max_length=20, choices=subjectchoice)
    content = models.TextField(max_length=1000, default='해당 과목 분석 작성')

    def subjectimage(self):
        return subjectdictionary[self.subject] if self.subject else None
