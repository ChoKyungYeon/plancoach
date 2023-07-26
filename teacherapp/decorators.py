from django.shortcuts import get_object_or_404

from accountapp.models import CustomUser
from plancoach.decorators import Decorators


def TeacherDashboardDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(CustomUser, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.owner_filter(allow_superuser=True)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

