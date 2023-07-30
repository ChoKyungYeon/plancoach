from consult_feedbackapp.models import Consult_feedback
from plancoach.decorators import *


def Feedback_likeDecorator(func):
    def decorated(request, *args, **kwargs):
        redirect = expire_redirector(request.user, request.GET.get('feedback_pk'), Consult_feedback, 'consult')
        if redirect:
            return redirect

        decorators=Decorators(request.user, Consult_feedback.objects.get(pk=request.GET.get('feedback_pk')).consult)
        decorators.update()
        permission_checks = [
            decorators.object_filter(allow_object= ['extended','unextended']),
            decorators.member_filter(role='student', allow_superuser=False),
        ]
        for check in permission_checks:
            if check is not None:
                return check

        redirect = expire_redirector(request.user, request.GET.get('feedback_pk'), Consult_feedback, 'consult')
        if redirect:
            return redirect

        return func(request, *args, **kwargs)
    return decorated