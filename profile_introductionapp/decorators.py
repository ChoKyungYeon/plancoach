from django.http import HttpResponseForbidden
from profile_introductionapp.models import Profile_introduction


def profile_introduction_ownership_required(func):
    def decorated(request,*args, **kwargs):
        profile_introduction = Profile_introduction.objects.get(pk=kwargs['pk'])
        if not profile_introduction.profile.customuser == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated
