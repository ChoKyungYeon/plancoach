from consult_qnaapp.models import Consult_qna
from plancoach.decorators import *


def Qna_likeDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector( request.GET.get('qna_pk'), Consult_qna, 'consult')
        if redirect:
            return redirect

        decorators=Decorators(request.user, Consult_qna.objects.get(pk=request.GET.get('qna_pk')).consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='student', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check

        redirect = expire_redirector( request.GET.get('qna_pk'), Consult_qna, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated