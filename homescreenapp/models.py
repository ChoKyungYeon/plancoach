from django.db import models


class Pageview(models.Model):
    #uuid
    date = models.DateField(unique=True)
    count = models.IntegerField(default=0)