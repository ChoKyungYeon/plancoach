from django.http import HttpResponseForbidden
from consultapp.models import Consult





def is_teacher(func):
    def decorated(request,*args, **kwargs):
        if request.user.state == 'student':
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated




