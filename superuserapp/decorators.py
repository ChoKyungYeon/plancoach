from plancoach.decorators import Decorators


def SuperuserDashboardDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, None)
        permission_checks = [
            decorators.step_filter( allow_teacher=[], allow_student=[], allow_superuser=True)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated
