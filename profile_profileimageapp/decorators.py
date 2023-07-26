from django.shortcuts import get_object_or_404

from plancoach.decorators import Decorators
from profile_profileimageapp.models import Profile_profileimage


def Profile_profileimageEditDecorater(func):
    def decorated(request, *args, **kwargs):
        decorators=Decorators(request.user, get_object_or_404(Profile_profileimage, pk=kwargs['pk']).profile)
        permission_checks = [
            decorators.member_filter(role='teacher', allow_superuser=False)
        ]
        for check in permission_checks:
            if check is not None:
                return check
        return func(request, *args, **kwargs)
    return decorated