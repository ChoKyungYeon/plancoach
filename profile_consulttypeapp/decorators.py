from django.http import HttpResponseForbidden
from profile_consulttypeapp.models import Profile_consulttype


def profile_consulttype_ownership_required(func):
    def decorated(request,*args, **kwargs):
        profile_consulttype = Profile_consulttype.objects.get(pk=kwargs['pk'])
        if not profile_consulttype.profile.customuser == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated
