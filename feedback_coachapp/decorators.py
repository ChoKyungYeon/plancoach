from django.shortcuts import get_object_or_404

from consult_feedbackapp.models import Consult_feedback
from feedback_coachapp.models import Feedback_coach
from plancoach.decorators import *


def Feedback_coachCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector( kwargs['pk'], Consult_feedback, 'consult')
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
        redirect = expire_redirector( kwargs['pk'], Consult_feedback, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated

def Feedback_coachUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector( kwargs['pk'], Feedback_coach, 'consult')
        if redirect:
            return redirect

        decorators=Decorators(request.user, get_object_or_404(Feedback_coach, pk=kwargs['pk']).consult_feedback.consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='teacher', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        redirect = expire_redirector( kwargs['pk'], Feedback_coach, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated

def Feedback_coachDeleteDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector( kwargs['pk'], Feedback_coach, 'consult')
        if redirect:
            return redirect

        decorators=Decorators(request.user, get_object_or_404(Feedback_coach, pk=kwargs['pk']).consult_feedback.consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='teacher', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        redirect = expire_redirector( kwargs['pk'], Feedback_coach, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated