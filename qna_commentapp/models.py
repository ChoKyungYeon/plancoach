from datetime import datetime, timedelta

from django.db import models
import uuid
from accountapp.models import CustomUser
from consult_qnaapp.models import Consult_qna
from plancoach.utils import time_before


class Qna_comment(models.Model):
    #uuid
    consult_qna = models.ForeignKey(Consult_qna, on_delete=models.CASCADE, related_name='qna_comment')
    customuser = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='qna_comment')
    image = models.ImageField(upload_to='qna_comment/', null=True, blank=True)
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def created_before(self):
        return time_before(self.created_at)