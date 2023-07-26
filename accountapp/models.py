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
        return f"[{self.username}] {self.userrealname}"

    def user_phonenumber(self):
        username = self.username
        return f"{username[:3]}-{username[3:7]}-{username[7:]}"


    def teacher_step(self):
        return 'ongoing' if self.application_teacher.all() or self.consult_teacher.all() else 'end'

    def student_step(self):
        application = getattr(self, 'application_student', None)
        if application:
            return 'applied' if application.state == 'applied' else 'matching'

        consult = getattr(self, 'consult_student', None)
        if consult:
            return 'new' if consult.state == 'new' else 'ongoing'

        if getattr(self, 'refusal', None):
            return 'end'

        teacherapply = getattr(self, 'teacherapply', None)
        if teacherapply and teacherapply.is_done:
            return 'teacherapplied'

        if self.refund.all().filter(is_given=False).first():
            return 'refund'

        return 'initial'


    def can_apply(self):
        if self.state == 'student':
            if self.student_step() in ['initial', 'end']:
                return True
        return False

    def can_delete(self):
        if self.state == 'student':
            if self.student_step() in ['initial', 'end']:
                return True
        elif self.state == 'teacher':
            if self.teacher_step() in ['end']:
                return True
        return False


    def delete(self, *args, **kwargs):
        [refund.delete() for refund in self.refund.all() if not refund.salary]
        super().delete(*args, **kwargs)