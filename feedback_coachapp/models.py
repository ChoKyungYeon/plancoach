from django.db import models
from consult_feedbackapp.models import Consult_feedback
from plancoach.choice import subjectchoice
from plancoach.variables import subjectdictionary
import uuid

class Feedback_coach(models.Model):
    #uuid
    consult_feedback = models.ForeignKey(Consult_feedback, on_delete=models.CASCADE, related_name='feedback_coach')
    subject = models.CharField(max_length=20, choices=subjectchoice)
    content = models.TextField(max_length=1000,null=True)

    def subjectimage(self):
        return subjectdictionary[self.subject] if self.subject else None
