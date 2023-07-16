from django.db import models

from accountapp.models import CustomUser
from consult_qnaapp.models import Consult_qna

class Qna_like(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='qna_like')
    consult_qna = models.ForeignKey(Consult_qna, on_delete=models.CASCADE, related_name='qna_like')

    class Meta:
        unique_together =('student', 'consult_qna')