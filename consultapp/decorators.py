from django.shortcuts import get_object_or_404

from accountapp.models import CustomUser
from applicationapp.models import Application
from consultapp.models import Consult
from plancoach.decorators import *


def ConsultCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector( kwargs['pk'], Application, 'application')
        if redirect:
            return redirect

        decorators=Decorators(request.user, get_object_or_404(Application, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['matching']),
            decorators.member_filter(role='teacher', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check

        redirect = expire_redirector( kwargs['pk'], Application, 'application')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated

def ConsultInfoUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector( kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        decorators=Decorators(request.user, get_object_or_404(Consult, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= 'all'),
            decorators.member_filter(role='teacher', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)

        redirect = expire_redirector( kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

    return decorated

def ConsultDashboardDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector( kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        decorators=Decorators(request.user, get_object_or_404(Consult, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= 'all'),
            decorators.member_filter(role='member', allow_superuser=True),
        ]
        for check in permission_checks:
            if check is not None:
                return check

        redirect = expire_redirector( kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated

def ConsultApplyDetailDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector( kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        decorators=Decorators(request.user, get_object_or_404(Consult, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= 'all'),
            decorators.member_filter(role='member', allow_superuser=True),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        redirect = expire_redirector( kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated


def ConsultPaymentListDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector( kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        decorators=Decorators(request.user, get_object_or_404(Consult, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= 'all'),
            decorators.member_filter(role='student', allow_superuser=True),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        redirect = expire_redirector( kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated

