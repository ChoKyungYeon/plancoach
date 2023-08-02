from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from plancoach.decorators import Decorators
from profile_introductionapp.models import Profile_introduction
from profileapp.models import Profile


def Profile_introductionEditDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(Profile_introduction, pk=kwargs['pk']).profile)
        permission_checks = [
            decorators.member_filter(role='teacher', allow_superuser=False),
            decorators.has_object('profile_introduction')
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def Profile_introductionCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(Profile, pk=kwargs['pk']))
        permission_checks = [
            decorators.member_filter(role='teacher', allow_superuser=False),
            decorators.has_object('profile_introduction')
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated