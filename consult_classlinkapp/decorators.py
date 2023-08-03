from django.shortcuts import get_object_or_404

from consult_classlinkapp.models import Consult_classlink
from consultapp.models import Consult
from plancoach.decorators import *


def Consult_classlinkCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector( kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        decorators=Decorators(request.user, get_object_or_404(Consult, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='teacher', allow_superuser=False),
            decorators.has_object('consult_classlink')
        ]
        for check in permission_checks:
            if check is not None:
                return check
        redirect = expire_redirector( kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated

def Consult_classlinkUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector( kwargs['pk'], Consult_classlink, 'consult')
        if redirect:
            return redirect
        decorators=Decorators(request.user, get_object_or_404(Consult_classlink, pk=kwargs['pk']).consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='teacher', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        redirect = expire_redirector( kwargs['pk'], Consult_classlink, 'consult')
        if redirect:
            return redirect
        return func(request, *args, **kwargs)
    return decorated