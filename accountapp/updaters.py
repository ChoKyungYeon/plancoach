from django.shortcuts import get_object_or_404

from accountapp.models import CustomUser
from plancoach.updaters import user_updater


def target_user_updater(func):
    def decorated(request,*args, **kwargs):
        target_user= get_object_or_404(CustomUser, pk=kwargs['pk'])
        user_updater(target_user)
        return func(request, *args, **kwargs)
    return decorated
