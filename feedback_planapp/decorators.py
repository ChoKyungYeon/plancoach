from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from feedback_planapp.models import Feedback_plan
from plancoach.decorators import Decorators


def Feedback_planUpdateDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(Feedback_plan, pk=kwargs['pk']).consult_feedback.consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='teacher', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def Feedback_planStateUpdateDecorater(func):
    def decorated(request, *args, **kwargs):
        plan=Feedback_plan.objects.get(pk=request.GET.get('plan_pk'))
        if not plan.can_check_plan:
            return HttpResponseForbidden()
        decorators=Decorators(request.user, plan.consult_feedback.consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='student', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated
