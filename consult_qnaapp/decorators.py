from django.shortcuts import get_object_or_404

from consult_qnaapp.models import Consult_qna
from consultapp.models import Consult
from plancoach.decorators import Decorators



def Consult_qnaCreateDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(Consult, pk=kwargs['pk']))
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

def Consult_qnaListDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(Consult, pk=kwargs['pk']))
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= 'all'),
            decorators.member_filter(role='member', allow_superuser=True),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated


def Consult_qnaUpdateDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(Consult_qna, pk=kwargs['pk']).consult)
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

def Consult_qnaDetailDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(Consult_qna, pk=kwargs['pk']).consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='member', allow_superuser=True),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated
