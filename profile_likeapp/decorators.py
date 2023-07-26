from plancoach.decorators import Decorators
from profile_likeapp.models import Profile_like


def Profile_likeDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, None)
        decorators.update()
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student= 'all', allow_superuser= False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated