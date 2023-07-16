from django.db import models

from applicationapp.models import Application
from plancoach.variables import current_datetime


class Application_refusal(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='application_refusal')
    content = models.CharField(max_length=15)

    def save(self, *args, **kwargs):
        created = not self.pk
        if created:
            application=self.application
            application.state='denied'
            application.updated_at=current_datetime
            application.save()
        super().save(*args, **kwargs)