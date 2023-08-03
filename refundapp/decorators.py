from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from consultapp.models import Consult
from plancoach.decorators import *
from refundapp.models import Refund


def RefundCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector( kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        consult = get_object_or_404(Consult, pk=kwargs['pk'])
        if consult.can_refund() == False:
            return HttpResponseForbidden()
        decorators=Decorators(request.user, consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['unextended','extended']),
            decorators.member_filter(role='student', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check

        redirect = expire_redirector( kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect
        return func(request, *args, **kwargs)
    return decorated

def RefundGuideDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector( kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        consult=get_object_or_404(Consult, pk=kwargs['pk'])
        if consult.can_refund() == False:
            return HttpResponseForbidden()
        decorators=Decorators(request.user,consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['unextended','extended']),
            decorators.member_filter(role='student', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        redirect = expire_redirector( kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated

def RefundStateUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        refund = Refund.objects.get(pk=request.GET.get('refund_pk'))
        if refund.is_given == True:
            return HttpResponseForbidden()
        decorators = Decorators(request.user, None)
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=[], allow_superuser=True)
        ]
        for check in permission_checks:
            if check is not None:
                return check

        return func(request, *args, **kwargs)
    return decorated


def RefundDetailDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(Refund, pk=kwargs['pk']))
        print(get_object_or_404(Refund, pk=kwargs['pk']).student)
        permission_checks = [

            decorators.member_filter(role='student', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def RefundPayDecorator(func):
    def decorated(request, *args, **kwargs):
        refund = get_object_or_404(Refund, pk=kwargs['pk'])
        if refund.is_given == True:
            return HttpResponseForbidden()
        decorators=Decorators(request.user, None)
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=[], allow_superuser=True)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

