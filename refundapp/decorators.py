from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from consultapp.models import Consult
from plancoach.decorators import Decorators
from refundapp.models import Refund


def RefundCreateDecorater(func):
    def decorated(request, *args, **kwargs):
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

        return func(request, *args, **kwargs)
    return decorated

def RefundGuideDecorater(func):
    def decorated(request, *args, **kwargs):
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
        return func(request, *args, **kwargs)
    return decorated

def RefundStateUpdateDecorater(func):
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


def RefundDetailDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(Refund, pk=kwargs['pk']))
        permission_checks = [
            decorators.member_filter(role='student', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def RefundPayDecorater(func):
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

