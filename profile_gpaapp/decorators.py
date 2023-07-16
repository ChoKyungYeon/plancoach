from django.http import HttpResponseForbidden
from profile_gpaapp.models import Profile_gpa


def profile_gpa_ownership_required(func):
    def decorated(request,*args, **kwargs):
        profile_gpa = Profile_gpa.objects.get(pk=kwargs['pk'])
        if not profile_gpa.profile.customuser == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated
