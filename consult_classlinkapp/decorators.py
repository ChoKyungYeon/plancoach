from django.shortcuts import get_object_or_404

from consult_classlinkapp.models import Consult_classlink
from consultapp.models import Consult
from plancoach.decorators import Decorators


def Consult_classlinkCreateDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(Consult, pk=kwargs['pk']))
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

def Consult_classlinkUpdateDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(Consult_classlink, pk=kwargs['pk']).consult)
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