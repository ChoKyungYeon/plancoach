from django.db import models


class Document(models.Model):
    termofuse = models.FileField(upload_to='document/')
    privacypolicy = models.FileField(upload_to='document/')
    kakaotalk = models.TextField(max_length=200)
    termofuse_updated = models.DateField()
    privacypolicy_updated = models.DateField()

