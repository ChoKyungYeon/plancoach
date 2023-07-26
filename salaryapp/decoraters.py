from datetime import datetime

from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from plancoach.decorators import Decorators
from plancoach.utils import salaryday_calculator
from salaryapp.models import Salary


def SalaryDetailDecorater(func):
    def decorated(request, *args, **kwargs):
        salary=get_object_or_404(Salary, pk=kwargs['pk'])
        if not salary.is_given == True:
            return HttpResponseForbidden()
        decorators=Decorators(request.user,salary)
        permission_checks = [
            decorators.member_filter(role='teacher', allow_superuser=True),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def SalaryExpectedDecorater(func):
    def decorated(request, *args, **kwargs):
        salary=get_object_or_404(Salary, pk=kwargs['pk'])
        if salary.is_given == True or salary.salaryday != salaryday_calculator(datetime.now().date()):
            return HttpResponseForbidden()
        decorators=Decorators(request.user,salary)
        permission_checks = [
            decorators.member_filter(role='teacher', allow_superuser=True),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def SalaryPayDecorater(func):
    def decorated(request, *args, **kwargs):
        salary=get_object_or_404(Salary, pk=kwargs['pk'])
        if salary.is_given == True or salary.salaryday > datetime.now().date():
            return HttpResponseForbidden()
        decorators=Decorators(request.user,salary)
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=[], allow_superuser=True)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def SalaryStateUpdateDecorater(func):
    def decorated(request, *args, **kwargs):
        salary=get_object_or_404(Salary, pk=kwargs['pk'])
        if salary.is_given == True or salary.salaryday > datetime.now().date():
            return HttpResponseForbidden()
        decorators=Decorators(request.user,salary)
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=[], allow_superuser=True)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated