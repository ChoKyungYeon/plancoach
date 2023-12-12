from django.db import models
import uuid

class Document(models.Model):
    #uuid
    termofuse = models.TextField(max_length=200, null=True, blank=True)
    privacypolicy = models.TextField(max_length=200, null=True, blank=True)
    announcement = models.TextField(max_length=200,null=True, blank=True)
    blog = models.TextField(max_length=200,null=True, blank=True)
    instagram = models.TextField(max_length=200,null=True, blank=True)
    kakaotalk = models.TextField(max_length=200,null=True, blank=True)
    phonenumber = models.CharField(max_length=20,null=True, blank=True)


