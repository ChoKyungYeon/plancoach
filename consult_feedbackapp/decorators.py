from django.shortcuts import get_object_or_404

from consult_feedbackapp.models import Consult_feedback
from consultapp.models import Consult
from plancoach.decorators import *


def Consult_feedbackCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector(request.user, kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        decorators=Decorators(request.user, get_object_or_404(Consult, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='teacher', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        redirect = expire_redirector(request.user, kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated

def Consult_feedbackListDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector(request.user, kwargs['pk'], Consult, 'consult')
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
        redirect = expire_redirector(request.user, kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated


def Consult_feedbackDeleteDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector(request.user, kwargs['pk'], Consult_feedback, 'consult')
        if redirect:
            return redirect

        decorators=Decorators(request.user, get_object_or_404(Consult_feedback, pk=kwargs['pk']).consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='teacher', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check

        redirect = expire_redirector(request.user, kwargs['pk'], Consult_feedback, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated


def Consult_feedbackUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector(request.user, kwargs['pk'], Consult_feedback, 'consult')
        if redirect:
            return redirect


        decorators=Decorators(request.user, get_object_or_404(Consult_feedback, pk=kwargs['pk']).consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='teacher', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check

        redirect = expire_redirector(request.user, kwargs['pk'], Consult_feedback, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated

def Consult_feedbackContentUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector(request.user, kwargs['pk'], Consult_feedback, 'consult')
        if redirect:
            return redirect

        decorators=Decorators(request.user, get_object_or_404(Consult_feedback, pk=kwargs['pk']).consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='teacher', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check

        redirect = expire_redirector(request.user, kwargs['pk'], Consult_feedback, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated


def Consult_feedbackBaseDetailDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector(request.user, kwargs['pk'], Consult_feedback, 'consult')
        if redirect:
            return redirect

        decorators=Decorators(request.user, get_object_or_404(Consult_feedback, pk=kwargs['pk']).consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='member', allow_superuser=True),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        redirect = expire_redirector(request.user, kwargs['pk'], Consult_feedback, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated


