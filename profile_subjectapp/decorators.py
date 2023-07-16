from django.http import HttpResponseForbidden
from profile_subjectapp.models import Profile_subject


def profile_subject_ownership_required(func):
    def decorated(request,*args, **kwargs):
        profile_subject = Profile_subject.objects.get(pk=kwargs['pk'])
        if not profile_subject.profile.customuser == request.user:
            return HttpResponseForbidden()
        return func(request, *args, **kwargs)
    return decorated
