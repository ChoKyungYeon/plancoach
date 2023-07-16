from django.shortcuts import get_object_or_404

from consultapp.models import Consult
from plancoach.updaters import user_updater


def target_consult_updater(func):
    def decorated(request,*args, **kwargs):
        target_consult= get_object_or_404(Consult, pk=kwargs['pk'])
        user_updater(target_consult.teacher)
        return func(request, *args, **kwargs)
    return decorated
