from django.http import HttpResponseForbidden
from applicationapp.models import Application


def application_ownership_required(func):
    def decorated(request,*args, **kwargs):
        application = Application.objects.get(pk=kwargs['pk'])
        if not application.student == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated
