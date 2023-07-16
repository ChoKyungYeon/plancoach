from django.http import HttpResponseForbidden
from consultapp.models import Consult





def is_teacher(func):
    def decorated(request,*args, **kwargs):
        if request.user.state == 'student':
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated


def is_student(func):
    def decorated(request,*args, **kwargs):
        if not request.user.state == 'student':
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated

def is_superuser(func):
    def decorated(request,*args, **kwargs):
        if request.user.state == 'student' or request.user.state == 'teacher':
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated






def is_consult_teacher(func):
    def decorated(request, *args, **kwargs):
        consult = Consult.objects.get(pk=kwargs['pk'])
        if not request.user == consult.teacher:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated

def is_consult_student(func):
    def decorated(request, *args, **kwargs):
        consult = Consult.objects.get(pk=kwargs['pk'])
        if not request.user == consult.student:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated



