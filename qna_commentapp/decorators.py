from django.shortcuts import get_object_or_404

from consult_qnaapp.models import Consult_qna
from plancoach.decorators import Decorators
from qna_commentapp.models import Qna_comment


def Qna_commentCreateDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(Consult_qna, pk=kwargs['pk']).consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='memeber', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def Qna_commentUpdateDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(Qna_comment, pk=kwargs['pk']).consult_qna.consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='memeber', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated
