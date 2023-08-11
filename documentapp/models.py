from django.db import models


class Document(models.Model):
    termofuse_link = models.TextField(max_length=200, null=True, blank=True)
    privacypolicy_link = models.TextField(max_length=200, null=True, blank=True)
    announcement_link = models.TextField(max_length=200,null=True, blank=True)
    email = models.TextField(max_length=200,null=True, blank=True)
    kakaotalk = models.TextField(max_length=200,null=True, blank=True)
    phonenumber = models.CharField(max_length=20,null=True, blank=True)

    @property
    def email_link(self):
        return f'mailto:{self.email}'

