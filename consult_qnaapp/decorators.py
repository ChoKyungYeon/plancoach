from django.shortcuts import get_object_or_404

from consult_qnaapp.models import Consult_qna
from consultapp.models import Consult
from plancoach.decorators import *



def Consult_qnaCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector(request.user, kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        decorators=Decorators(request.user, get_object_or_404(Consult, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='student', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check

        redirect = expire_redirector(request.user, kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated

def Consult_qnaListDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector(request.user, kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        decorators=Decorators(request.user, get_object_or_404(Consult, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= 'all'),
            decorators.member_filter(role='member', allow_superuser=True),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        redirect = expire_redirector(request.user, kwargs['pk'], Consult, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated


def Consult_qnaUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector(request.user, kwargs['pk'], Consult_qna, 'consult')
        if redirect:
            return redirect

        decorators=Decorators(request.user, get_object_or_404(Consult_qna, pk=kwargs['pk']).consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='student', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check

        redirect = expire_redirector(request.user, kwargs['pk'], Consult_qna, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated

def Consult_qnaDetailDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector(request.user, kwargs['pk'], Consult_qna, 'consult')
        if redirect:
            return redirect

        decorators=Decorators(request.user, get_object_or_404(Consult_qna, pk=kwargs['pk']).consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='member', allow_superuser=True),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        redirect = expire_redirector(request.user, kwargs['pk'], Consult_qna, 'consult')
        if redirect:
            return redirect
        return func(request, *args, **kwargs)
    return decorated
