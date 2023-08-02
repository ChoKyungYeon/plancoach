from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.generic import CreateView, UpdateView, DeleteView

from profile_consulttypeapp.decorators import *
from profile_consulttypeapp.forms import Profile_consulttypeCreateForm
from profile_consulttypeapp.models import Profile_consulttype
from django.utils.decorators import method_decorator

@method_decorator(never_cache, name='dispatch')
@method_decorator(login_required, name='dispatch')
@method_decorator(Profile_consulttypeEditDecorator, name='dispatch')
class Profile_consulttypeUpdateView(UpdateView):
    model = Profile_consulttype
    context_object_name = 'target_profile_consulttype'
    form_class = Profile_consulttypeCreateForm
    template_name = 'profile_consulttypeapp/update.html'
    def get_success_url(self):
        return reverse_lazy('profileapp:detail', kwargs={'pk': self.object.profile.pk})

