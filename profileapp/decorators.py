from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from accountapp.models import CustomUser
from plancoach.decorators import Decorators
from profileapp.models import Profile
from teacherapplyapp.models import Teacherapply


def Profile_instanceCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(Profile, pk=kwargs['pk']))
        permission_checks = [
            decorators.member_filter(role='teacher', allow_superuser=False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated


def Profile_instanceManageDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, None)
        permission_checks = [
            decorators.step_filter( allow_teacher=[], allow_student=[], allow_superuser=True)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated


def ProfileCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        teacherapply = get_object_or_404(Teacherapply, pk=kwargs['pk'])
        if teacherapply.is_done == False:
            return HttpResponseForbidden()
        decorators=Decorators(request.user,None)
        permission_checks = [
            decorators.step_filter( allow_teacher=[], allow_student=[], allow_superuser=True)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def ProfileDeleteDecorator(func):
    def decorated(request, *args, **kwargs):
        teacher=get_object_or_404(Profile, pk=kwargs['pk']).teacher
        decorators=Decorators(request.user, teacher)
        decorators.update()
        if teacher.can_delete() == False:
            return HttpResponseForbidden()
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=[], allow_superuser=True)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def ProfileTuitionUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        profile=get_object_or_404(Profile, pk=kwargs['pk'])
        decorators=Decorators(request.user, profile)
        if profile.is_payment_updated_possible() == False:
            return HttpResponseForbidden()
        permission_checks = [
            decorators.member_filter(role='teacher', allow_superuser=False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def ProfileDetailDecorator(func):
    def decorated(request, *args, **kwargs):
        if request.user.is_authenticated:
            decorators=Decorators(request.user,None)
            decorators.request_user_update()
        return func(request, *args, **kwargs)
    return decorated

def ProfileStateUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user,CustomUser.objects.get(pk=request.GET.get('user_pk')).profile)
        permission_checks = [
            decorators.member_filter(role='teacher', allow_superuser=True)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated
