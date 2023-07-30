from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import RedirectView

from profile_likeapp.decorators import Profile_likeDecorator
from profile_likeapp.models import Profile_like
from profileapp.models import Profile
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
@method_decorator(Profile_likeDecorator, name='dispatch')
class Profile_likeView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('profileapp:detail', kwargs={'pk':self.request.GET.get('profile_pk')})

    def get(self, request, *args, **kwargs):
        profile=get_object_or_404(Profile, pk=self.request.GET.get('profile_pk'))
        customuser=self.request.user

        profile_like = Profile_like.objects.filter(student=customuser, profile=profile)

        if profile_like.exists():
            profile_like.delete()
        else:
            Profile_like.objects.create(student=customuser, profile=profile)
        return super(Profile_likeView, self).get(request, *args, **kwargs)


