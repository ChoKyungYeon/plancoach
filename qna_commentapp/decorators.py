from django.shortcuts import get_object_or_404

from consult_qnaapp.models import Consult_qna
from plancoach.decorators import *
from qna_commentapp.models import Qna_comment


def Qna_commentCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector(request.user, kwargs['pk'], Consult_qna, 'consult')
        if redirect:
            return redirect
        decorators=Decorators(request.user, get_object_or_404(Consult_qna, pk=kwargs['pk']).consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='memeber', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        redirect = expire_redirector(request.user, kwargs['pk'], Consult_qna, 'consult')
        if redirect:
            return redirect
        return func(request, *args, **kwargs)
    return decorated

def Qna_commentUpdateDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector(request.user, kwargs['pk'],Qna_comment, 'consult')
        if redirect:
            return redirect
        decorators=Decorators(request.user, get_object_or_404(Qna_comment, pk=kwargs['pk']).consult_qna.consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='memeber', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        redirect = expire_redirector(request.user, kwargs['pk'], Qna_comment, 'consult')
        if redirect:
            return redirect
        return func(request, *args, **kwargs)
    return decorated
