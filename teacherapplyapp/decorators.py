from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from accountapp.models import CustomUser
from plancoach.decorators import Decorators
from teacherapplyapp.models import Teacherapply


def TeacherapplySchoolimageCreateDecorater(func):
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

def TeacherapplyUserimageCreateDecorater(func):
    def decorated(request, *args, **kwargs):
        teacherapply=get_object_or_404(Teacherapply, pk=kwargs['pk'])
        if teacherapply.has_userimage == True:
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

def TeacherapplyBankCreateDecorater(func):
    def decorated(request, *args, **kwargs):
        teacherapply=get_object_or_404(Teacherapply, pk=kwargs['pk'])
        if teacherapply.has_userimage != True or teacherapply.has_bank == True:
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

def TeacherapplyInfoCreateDecorater(func):
    def decorated(request, *args, **kwargs):
        teacherapply=get_object_or_404(Teacherapply, pk=kwargs['pk'])
        if teacherapply.has_bank != True or teacherapply.is_done == True:
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

def TeacherapplyGuideDecorater(func):
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

def TeacherapplyDetailDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(Teacherapply, pk=kwargs['pk']).customuser)
        decorators.update()
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=['teacherapplied'], allow_superuser=False),
            decorators.owner_filter(allow_superuser=False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def TeacherapplyRegisterDecorater(func):
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

def TeacherapplyDeleteDecorater(func):
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


