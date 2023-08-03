from datetime import datetime, timedelta
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404

from accountapp.models import CustomUser
from applicationapp.models import Application
from consultapp.models import Consult
from phonenumberapp.models import Phonenumber
from plancoach.utils import create_refusal


class Decorators:
    def __init__(self, user, obj):
        self.user = user
        self.obj = obj

    def update(self):
        if isinstance(self.obj, Application):
            self.application_update(self.obj)
        elif isinstance(self.obj, Consult):
            self.consult_update(self.obj)
        elif isinstance(self.obj, CustomUser):
            self.user_update(self.obj)


    def application_update(self,application): #deploy check
        with transaction.atomic():
            target_state = application.state
            updated_at = application.updated_at
            updated_interval = datetime.now() - updated_at
            if target_state == 'applied' and updated_interval > timedelta(hours=24): #minute 24
                create_refusal(application,'기간 내 신청이 확인되지 않았습니다.','matching')
            elif target_state == 'matching' and updated_interval > timedelta(hours=168): #minute 168
                create_refusal(application,'기간 내 매칭이 성사되지 않았습니다.','matching')

    def consult_update(self,consult): #deploy check
        with transaction.atomic():
            today = datetime.now().date()
            extenddate = consult.extenddate()
            extend_enddate = consult.extend_enddate()
            target_state = consult.state
            created_interval=datetime.now() - consult.created_at
            if target_state == 'new' and created_interval > timedelta(hours=96): #hour 48
                create_refusal(consult, '기간 내 입금이 완료되지 않았습니다.','matching')
            elif target_state == 'unextended' and extenddate <= today: # extenddate <= today
                create_refusal(consult, None,'consult')
            elif target_state == 'extended':
                if extend_enddate < today:
                    create_refusal(consult, None,'consult')
                elif extenddate <= today <= extend_enddate:
                    consult.startdate = extenddate
                    consult.state = 'unextended'
                    consult.save()

    def user_update(self,user):
        with transaction.atomic():
            if user.state == 'student':
                application = getattr(user, 'application_student', None)
                consult = getattr(user, 'consult_student', None)
                if application:
                    self.application_update(application)
                if consult:
                    self.consult_update(consult)

            elif user.state == 'teacher':
                applications = getattr(user, 'application_teacher').all()
                consults = getattr(user, 'consult_teacher').all()
                for application in applications:
                    self.application_update(application)
                for consult in consults:
                    self.consult_update(consult)

    def request_user_update(self):
        self.user_update(self.user)

    def phonenumber_update(self): #deploy check
        for phonenumber in Phonenumber.objects.filter(is_verified=False):
            if datetime.now() - phonenumber.created_at > timedelta(minutes=3):
                phonenumber.delete()



    def object_filter(self, allow_object):
        if not allow_object == 'all':
            return HttpResponseForbidden() if not self.obj.state in allow_object else None


    def has_object(self, object):
        if hasattr(self.obj, object):
            return HttpResponseForbidden()


    def step_filter(self, allow_teacher, allow_student, allow_superuser):
        if self.user.state == 'superuser' and not allow_superuser:
            return HttpResponseForbidden()
        if not allow_teacher == 'all' and self.user.state == 'teacher' and self.user.teacher_step() not in allow_teacher:
            return HttpResponseForbidden()
        if not allow_student == 'all' and self.user.state == 'student' and self.user.student_step() not in allow_student:
            return HttpResponseForbidden()


    def member_filter(self, role, allow_superuser):
        if not self.obj:
            return HttpResponseForbidden()
        if not (allow_superuser and self.user.state == 'superuser'):
            if role == 'customuser' and self.user != self.obj.customuser:
                return HttpResponseForbidden()
            elif role == 'teacher' and self.user != self.obj.teacher:
                return HttpResponseForbidden()
            elif role == 'student' and self.user != self.obj.student:
                return HttpResponseForbidden()
            elif role == 'member' and (self.user != self.obj.teacher and self.user != self.obj.student):
                return HttpResponseForbidden()

    def owner_filter(self, allow_superuser):
        if not (allow_superuser and self.user.state == 'superuser'):
            if not self.user == self.obj:
                return HttpResponseForbidden()

    def owner_filter(self, allow_superuser):
        if not (allow_superuser and self.user.state == 'superuser'):
            if not self.user == self.obj:
                return HttpResponseForbidden()

def expire_redirector(pk, model, type):
    redirect_dict = {
        'application': 'applicationapp:expire',
        'consult': 'consultapp:expire',
        'teacherapply': 'teacherapplyapp:expire',
        'accountcreate': 'accountapp:login',
    }
    try:
        get_object_or_404(model, pk=pk)
        return None
    except:
        return redirect(redirect_dict[type]) if type in redirect_dict else None