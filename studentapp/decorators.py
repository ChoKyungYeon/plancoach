from django.shortcuts import get_object_or_404

from accountapp.models import CustomUser
from plancoach.decorators import Decorators


def StudentDashboardDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user,get_object_or_404(CustomUser, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student='all', allow_superuser=True),
            decorators.owner_filter( allow_superuser=True)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def StudentRefundListDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user,get_object_or_404(CustomUser, pk=kwargs['pk']))
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student='all', allow_superuser=False),
            decorators.owner_filter(allow_superuser=False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated