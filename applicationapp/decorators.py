from django.shortcuts import get_object_or_404, redirect

from accountapp.models import CustomUser
from applicationapp.models import Application
from plancoach.decorators import *

def ApplicationCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(CustomUser, pk=kwargs['pk']).profile)
        decorators.request_user_update()
        permission_checks = [
            decorators.object_filter(allow_object= ['abled']),
            decorators.step_filter(allow_teacher=[], allow_student= ['initial','end'], allow_superuser= False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def ApplicationDeleteDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector(request.user, kwargs['pk'], Application, 'application')
        if redirect:
            return redirect

        decorators=Decorators(request.user, get_object_or_404(Application, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['applied']),
            decorators.member_filter(role='student', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        redirect = expire_redirector(request.user, kwargs['pk'], Application, 'application')
        if redirect:
            return redirect
        return func(request, *args, **kwargs)
    return decorated

def ApplicationUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector(request.user, kwargs['pk'], Application, 'application')
        if redirect:
            return redirect

        decorators=Decorators(request.user,get_object_or_404(Application, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object=['applied']),
            decorators.member_filter(role='student', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        redirect = expire_redirector(request.user, kwargs['pk'], Application, 'application')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated


def ApplicationDetailDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector(request.user, kwargs['pk'], Application, 'application')
        if redirect:
            return redirect

        decorators=Decorators(request.user,get_object_or_404(Application, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object='all'),
            decorators.member_filter(role='member', allow_superuser=True)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        redirect = expire_redirector(request.user, kwargs['pk'], Application, 'application')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated

def ApplicationStateUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector(request.user,request.GET.get('application_pk'), Application, 'application')
        if redirect:
            return redirect
        decorators=Decorators(request.user, Application.objects.get(pk=request.GET.get('application_pk')))
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['applied']),
            decorators.member_filter(role='teacher', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check

        redirect = expire_redirector(request.user,request.GET.get('application_pk'), Application, 'application')
        if redirect:
            return redirect
        return func(request, *args, **kwargs)
    return decorated

def ApplicationGuideDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators = Decorators(request.user, get_object_or_404(CustomUser, pk=kwargs['pk']).profile)
        decorators.request_user_update()
        permission_checks = [
            decorators.object_filter(allow_object=['abled']),
            decorators.step_filter(allow_teacher=[], allow_student=['initial','end'], allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def ApplicationResultDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators = Decorators(request.user, None)
        decorators.request_user_update()
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=['applied'], allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated
