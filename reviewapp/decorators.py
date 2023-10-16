from django.http import HttpResponseForbidden

from plancoach.decorators import Decorators


def ReviewDeleteDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, None)
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=[], allow_superuser=True)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def ReviewManageDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, None)
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=[], allow_superuser=True)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

def ReviewListDecorator(func):
    def decorated(request, *args, **kwargs):
        if request.user.is_authenticated:
            decorators=Decorators(request.user,None)
            decorators.request_user_update()
        return func(request, *args, **kwargs)
    return decorated

def ReviewCreateDecorator(func):
    def decorated(request, *args, **kwargs):
        user = request.user
        if user.can_review() == False:
            return HttpResponseForbidden()
        decorators = Decorators(user, None)
        decorators.request_user_update()
        permission_checks = [
            decorators.step_filter(allow_teacher=[], allow_student=['ongoing'], allow_superuser=False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated
