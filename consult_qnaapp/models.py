from django.db import models
from consultapp.models import Consult
from plancoach.utils import time_before
import uuid

class Consult_qna(models.Model):
    #uuid
    consult = models.ForeignKey(Consult, on_delete=models.CASCADE, related_name='consult_qna')
    image = models.ImageField(upload_to='consult_qna/' ,null=True, blank=True)
    content = models.TextField(max_length=500)
    title = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    is_answered = models.BooleanField(default=False)

    def created_before(self):
        return time_before(self.created_at)