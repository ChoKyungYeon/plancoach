from django.db import models
import uuid

class Pageview(models.Model):
    #uuid
    date = models.DateField(unique=True)
    count = models.IntegerField(default=0)