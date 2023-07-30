from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from accountapp.models import CustomUser
from phonenumberapp.models import Phonenumber
from plancoach.decorators import Decorators


def AccountCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        phonenumber=get_object_or_404(Phonenumber, pk=kwargs['pk'])
        if phonenumber.is_verified == False:
            return HttpResponseForbidden()
        if request.session['verification_code'] != str(phonenumber.verification_code):
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated


def AccountNotificationUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user,CustomUser.objects.get(pk=request.GET.get('user_pk')))
        permission_checks = [
            decorators.owner_filter(allow_superuser=False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated


def AccountOwnerDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user,get_object_or_404(CustomUser, pk=kwargs['pk']))
        permission_checks = [
            decorators.owner_filter(allow_superuser=False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def AccountDeleteDecorator(func):
    def decorated(request, *args, **kwargs):
        target_user=get_object_or_404(CustomUser, pk=kwargs['pk'])
        decorators=Decorators(request.user,get_object_or_404(CustomUser, pk=kwargs['pk']))
        decorators.update()
        if target_user.can_delete() != True:
            return HttpResponseForbidden()
        permission_checks = [
            decorators.owner_filter(allow_superuser=False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def AccountGetDeleteDecorator(func):
    def decorated(request, *args, **kwargs):
        target_user=get_object_or_404(CustomUser, pk=kwargs['pk'])
        decorators=Decorators(request.user,get_object_or_404(CustomUser, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.owner_filter(allow_superuser=False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated