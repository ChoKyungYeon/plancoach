from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from plancoach.decorators import Decorators
from profile_scholarshipapp.models import Profile_scholarship


def Profile_scholarshipEditDecorator(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(Profile_scholarship, pk=kwargs['pk']).profile)
        permission_checks = [
            decorators.member_filter(role='teacher', allow_superuser=False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated

