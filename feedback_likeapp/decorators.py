from consult_feedbackapp.models import Consult_feedback
from plancoach.decorators import Decorators


def Feedback_likeDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, Consult_feedback.objects.get(pk=request.GET.get('feedback_pk')).consult)
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