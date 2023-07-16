from django.http import HttpResponseForbidden
from profile_profileimageapp.models import Profile_profileimage


def profile_profileimage_ownership_required(func):
    def decorated(request,*args, **kwargs):
        profile_profileimage = Profile_profileimage.objects.get(pk=kwargs['pk'])
        if not profile_profileimage.profile.customuser == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated
