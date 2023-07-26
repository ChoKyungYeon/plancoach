from consult_qnaapp.models import Consult_qna
from plancoach.decorators import Decorators


def Qna_likeDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, Consult_qna.objects.get(pk=request.GET.get('qna_pk')).consult)
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