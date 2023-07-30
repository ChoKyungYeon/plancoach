from plancoach.decorators import Decorators


def HomescreenDecorator(func):
    def decorated(request, *args, **kwargs):
        if request.user.is_authenticated:
            decorators=Decorators(request.user,None)
            decorators.request_user_update()
        return func(request, *args, **kwargs)
    return decorated
