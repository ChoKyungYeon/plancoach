from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from phonenumberapp.models import Phonenumber
from plancoach.decorators import Decorators


def PhonenumberCreateDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, None)
        decorators.phonenumber_update()
        return func(request, *args, **kwargs)
    return decorated


def PhonenumberVerifyDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, None)
        decorators.phonenumber_update()
        return func(request, *args, **kwargs)
    return decorated