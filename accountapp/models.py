from django.db import models
from django.contrib.auth.models import AbstractUser

from plancoach.choice import userstatechoice


class CustomUser(AbstractUser):
    username = models.CharField(max_length=11, unique=True)
    userrealname = models.CharField(max_length=6)
    email = models.EmailField(max_length=40, unique=True)
    state = models.CharField(max_length=20, choices=userstatechoice, default='student')
    can_receive_notification = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.state}: {self.username}({self.userrealname})"

    def user_phonenumber(self):
        username = self.username
        return f"{username[:3]}-{username[3:7]}-{username[7:]}"

    def student_updater(self):
        application = getattr(self, 'application_student', None)
        consult = getattr(self, 'consult_student', None)
        if consult:
            consult.updater()
        if application:
            application.updater()

    def teacher_updater(self):
        applications = self.application_teacher.all()
        consults = self.consult_teacher.all()
        if consults:
            for consult in consults:
                consult.updater()
        if applications:
            for application in applications:
                application.updater()

    def student_step(self):
        if self.state == 'superuser':
            return 'superuser'
        if self.state == 'teacher':
            self.teacher_updater()
            return 'teacher'
        self.student_updater()
        application = getattr(self, 'application_student', None)
        consult = getattr(self, 'consult_student', None)
        refusal = getattr(self, 'refusal', None)
        refund = self.refund.all().filter(is_given=False).first()
        if application:
            if application.state == 'applied':
                return 'applied'
            else:
                return 'matching'
        elif consult:
            if consult.state == 'new':
                return 'new'
            else:
                return 'ongoing'
        elif refusal:
            return 'end'
        elif refund:
            return 'refund'
        else:
            return 'initial'

    def can_apply(self):
        return self.student_step() in ('initial', 'end')

    def delete(self, *args, **kwargs):
        [refund.delete() for refund in self.refund.all() if not refund.salary]
        super().delete(*args, **kwargs)
