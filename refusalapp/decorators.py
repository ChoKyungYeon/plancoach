from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from applicationapp.models import Application
from plancoach.decorators import Decorators
from teacherapplyapp.models import Teacherapply


def RefusalApplicationRefuseDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user,get_object_or_404(Application, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.member_filter(role='teacher', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def RefusalTeacherapplyRefuseDecorater(func):
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