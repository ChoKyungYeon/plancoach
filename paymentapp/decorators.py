from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from consultapp.models import Consult
from paymentapp.models import Payment
from plancoach.decorators import Decorators


def PaymentCreateDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(Consult, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['new','unextended']),
            decorators.member_filter(role='student', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def PaymentPayDecorater(func):
    def decorated(request, *args, **kwargs):
        payment=get_object_or_404(Payment, pk=kwargs['pk'])
        if payment.is_checked == True:
            return HttpResponseForbidden()
        decorators=Decorators(request.user, payment.consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object=['new','unextended']),
            decorators.member_filter(role='student', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def PaymentResultDecorater(func):
    def decorated(request, *args, **kwargs):
        payment = get_object_or_404(Payment, pk=kwargs['pk'])
        if payment.is_checked == False:
            return HttpResponseForbidden()
        decorators = Decorators(request.user, payment.consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object='all'),
            decorators.member_filter(role='student', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)

    return decorated


def PaymentContactDecorater(func):
    def decorated(request, *args, **kwargs):
        payment = get_object_or_404(Payment, pk=kwargs['pk'])
        if payment.is_checked == False or payment.is_paid_ok == True:
            return HttpResponseForbidden()
        decorators = Decorators(request.user, payment.consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object=['new','unextended']),
            decorators.member_filter(role='student', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)

    return decorated