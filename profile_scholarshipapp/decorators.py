from django.http import HttpResponseForbidden
from profile_scholarshipapp.models import Profile_scholarship


def profile_scholarship_ownership_required(func):
    def decorated(request,*args, **kwargs):
        profile_scholarship = Profile_scholarship.objects.get(pk=kwargs['pk'])
        if not profile_scholarship.profile.customuser == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated
