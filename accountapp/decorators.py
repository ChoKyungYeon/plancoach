from django.http import HttpResponseForbidden
from accountapp.models import CustomUser


def account_ownership_required(func):
    def decorated(request, *args, **kwargs):
        user = CustomUser.objects.get(pk=kwargs['pk'])
        if not request.user.state == 'superuser':
            if not user == request.user:
                return HttpResponseForbidden()
        return func(request, *args, **kwargs)

    return decorated
