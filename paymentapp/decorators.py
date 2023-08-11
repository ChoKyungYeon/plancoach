from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from consultapp.models import Consult
from paymentapp.models import Payment
from plancoach.decorators import *


def PaymentCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector( kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect
        consult=get_object_or_404(Consult, pk=kwargs['pk'])
        if consult.is_waiting() == True:
            return HttpResponseForbidden()
        decorators=Decorators(request.user, consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['new','unextended']),
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

def PaymentGuideDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector( kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        consult=get_object_or_404(Consult, pk=kwargs['pk'])
        if consult.is_waiting() == True:
            return HttpResponseForbidden()
        decorators=Decorators(request.user, consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['new','unextended']),
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


def PaymentStateUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        payment = Payment.objects.get(pk=request.GET.get('payment_pk'))
        if payment.is_paid_ok == True:
            return HttpResponseForbidden()
        decorators = Decorators(request.user, payment.consult)
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=[], allow_superuser=True)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)

    return decorated

def PaymentDeleteDecorator(func):
    def decorated(request, *args, **kwargs):
        payment = get_object_or_404(Payment, pk=kwargs['pk'])
        if payment.is_paid_ok == True:
            return HttpResponseForbidden()
        decorators = Decorators(request.user, payment.consult)
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=[], allow_superuser=True)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)

    return decorated

def PaymentPayDecorator(func):
    def decorated(request, *args, **kwargs):
        payment = get_object_or_404(Payment, pk=kwargs['pk'])
        if payment.is_paid_ok == True:
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
