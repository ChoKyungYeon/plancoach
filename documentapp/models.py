from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Document(models.Model):
    refund = models.FileField(upload_to='document/')
    termofuse = models.FileField(upload_to='document/')
    privacypolicy = models.FileField(upload_to='document/')
    kakaotalk = models.TextField(max_length=100)
    termofuse_updated = models.DateField()
    refund_updated = models.DateField()
    privacypolicy_updated = models.DateField()
