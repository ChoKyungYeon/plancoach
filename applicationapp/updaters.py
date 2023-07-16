from django.shortcuts import get_object_or_404

from accountapp.models import CustomUser
from applicationapp.models import Application
from plancoach.updaters import user_updater


def target_application_updater(func):
    def decorated(request,*args, **kwargs):
        target_application= get_object_or_404(Application, pk=kwargs['pk'])
        user_updater(target_application.teacher)
        return func(request, *args, **kwargs)
    return decorated
