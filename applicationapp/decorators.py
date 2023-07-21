from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from applicationapp.models import Application


def application_create_decorater(func):
    def decorated(request, *args, **kwargs):
        user = request.user
        target_step=user.step()
        if not target_step in ['initial','end'] :
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated

def application_delete_decorater(func):
    def decorated(request, *args, **kwargs):
        user = request.user
        target_step=user.step()
        application = get_object_or_404(Application, pk=kwargs['pk'])
        if not target_step == 'applied':
            return HttpResponseForbidden()
        elif not user == application.student:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated

def application_update_decorater(func):
    def decorated(request, *args, **kwargs):
        user = request.user
        target_step=user.step()
        application = get_object_or_404(Application, pk=kwargs['pk'])
        if not target_step == 'applied':
            return HttpResponseForbidden()
        elif not user == application.student:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated

def application_detail_decorater(func):
    def decorated(request, *args, **kwargs):
        user = request.user
        target_step=user.step()
        application = get_object_or_404(Application, pk=kwargs['pk'])
        application.updater()
        if target_step == 'teacher':
            return HttpResponseForbidden()
        elif not user == application.student:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated