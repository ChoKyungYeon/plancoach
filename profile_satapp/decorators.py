from django.http import HttpResponseForbidden
from profile_satapp.models import Profile_sat


def profile_sat_ownership_required(func):
    def decorated(request,*args, **kwargs):
        profile_sat = Profile_sat.objects.get(pk=kwargs['pk'])
        if not profile_sat.profile.customuser == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated
