from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from accountapp.models import CustomUser
from plancoach.decorators import Decorators, expire_redirector
from teacherapplyapp.models import Teacherapply


def TeacherapplySchoolimageCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(CustomUser, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=['initial','end'], allow_superuser=False),
            decorators.owner_filter(allow_superuser=False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def TeacherapplyUserimageCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        teacherapply=get_object_or_404(Teacherapply, pk=kwargs['pk'])
        if teacherapply.has_schoolimage == False:
            return HttpResponseForbidden()
        decorators=Decorators(request.user, teacherapply.customuser)
        decorators.update()
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=['initial','end'], allow_superuser=False),
            decorators.owner_filter(allow_superuser=False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def TeacherapplyBankCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        teacherapply=get_object_or_404(Teacherapply, pk=kwargs['pk'])
        if teacherapply.has_userimage == False:
            return HttpResponseForbidden()
        decorators=Decorators(request.user, teacherapply.customuser)
        decorators.update()
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=['initial','end'], allow_superuser=False),
            decorators.owner_filter(allow_superuser=False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def TeacherapplyInfoCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        teacherapply=get_object_or_404(Teacherapply, pk=kwargs['pk'])
        if teacherapply.has_bank == False:
            return HttpResponseForbidden()
        decorators=Decorators(request.user, teacherapply.customuser)
        decorators.update()
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=['initial','end'], allow_superuser=False),
            decorators.owner_filter(allow_superuser=False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def TeacherapplyGuideDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(CustomUser, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=['initial','end'], allow_superuser=False),
            decorators.owner_filter(allow_superuser=False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def TeacherapplyDetailDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector( kwargs['pk'], Teacherapply, 'teacherapply')
        if redirect:
            return redirect
        decorators=Decorators(request.user, get_object_or_404(Teacherapply, pk=kwargs['pk']).customuser)
        decorators.update()
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=['teacherapplied'], allow_superuser=False),
            decorators.owner_filter(allow_superuser=False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        redirect = expire_redirector( kwargs['pk'], Teacherapply, 'teacherapply')
        if redirect:
            return redirect
        return func(request, *args, **kwargs)
    return decorated

def TeacherapplyRegisterDecorator(func):
    def decorated(request, *args, **kwargs):
        teacherapply=get_object_or_404(Teacherapply, pk=kwargs['pk'])
        if teacherapply.is_done != True:
            return HttpResponseForbidden()
        decorators=Decorators(request.user, teacherapply.customuser)
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=[], allow_superuser=True),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def TeacherapplyDeleteDecorator(func):
    def decorated(request, *args, **kwargs):
        teacherapply=get_object_or_404(Teacherapply, pk=kwargs['pk'])
        if teacherapply.is_done != True:
            return HttpResponseForbidden()
        decorators=Decorators(request.user, teacherapply.customuser)
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=[], allow_superuser=True),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated


